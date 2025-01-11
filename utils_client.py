import time
import requests
import ctypes
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

ENDPOINT = "http://127.0.0.1:5000"


def hash_message(message, timings):
    t = time.time_ns()
    message = message.encode() if isinstance(message, str) else message
    hash_obj = hashlib.sha3_256()
    hash_obj.update(message)
    timings["client_hash_time"] = time.time_ns() - t
    return hash_obj.digest()


def read_and_encrypt_file(aes_key, raw_data, timings):
    start_time = time.time_ns()
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(raw_data, AES.block_size))
    timings["encryption_time"] = time.time_ns() - start_time
    return ciphertext, cipher.iv


def encapsulate_key(
    client_public_key,
    encapsulate_algorithm,
    cipher_text_bytes,
    shared_secret_bytes,
    timings,
):
    start_time = time.time_ns()
    encapsulated_key = ctypes.create_string_buffer(cipher_text_bytes)
    shared_secret = ctypes.create_string_buffer(shared_secret_bytes)
    result = encapsulate_algorithm(encapsulated_key, shared_secret, client_public_key)
    if result != 0:
        raise ValueError("Encapsulation failed")
    timings["encapsulate_key"] = time.time_ns() - start_time

    return encapsulated_key.raw, shared_secret.raw


def get_client_public_key(kem_name):
    payload = {"kem_name": kem_name}
    response = requests.post(f"{ENDPOINT}/keys", json=payload)
    data = response.json()
    if not data or "server_public_key" not in data:
        raise ValueError("Missing 'server_public_key' in response")
    return bytes.fromhex(data["server_public_key"])


def get_data_to_send(
    raw_data,
    server_public_key,
    encapsulation_algorithm,
    cipher_text_bytes,
    shared_secret_bytes,
    sign_algorithm,
    sign_public_key,
    sign_private_key,
    sign_bytes,
):
    timings = {}
    encapsulated_key, shared_secret = encapsulate_key(
        server_public_key,
        encapsulation_algorithm,
        cipher_text_bytes,
        shared_secret_bytes,
        timings,
    )
    ciphertext, iv = read_and_encrypt_file(shared_secret[:32], raw_data, timings)
    hashed_ciphertext = hash_message(ciphertext, timings)

    signature = sign_message(
        hashed_ciphertext, sign_algorithm, sign_private_key, sign_bytes, timings
    )
    return {
        "cipher_text": ciphertext.hex(),
        "iv": iv.hex(),
        "signature": signature.hex(),
        "secret_key": encapsulated_key.hex(),
        "sign_pub_key": sign_public_key.hex(),
        "timings": timings,
    }


def send_data(
    raw_data,
    kem_algo_name,
    kem_algorithm,
    kem_cipher_text_bytes,
    kem_shared_secret_bytes,
    sign_algorithm_name,
    sign_algorithm,
    sign_public_key,
    sign_private_key,
    sign_bytes,
):
    client_public_key = get_client_public_key(kem_algo_name)
    payload = get_data_to_send(
        raw_data,
        client_public_key,
        kem_algorithm,
        kem_cipher_text_bytes,
        kem_shared_secret_bytes,
        sign_algorithm,
        sign_public_key,
        sign_private_key,
        sign_bytes,
    )

    payload["kem_algo_name"] = kem_algo_name
    payload["sign_algorithm_name"] = sign_algorithm_name
    response = requests.post(f"{ENDPOINT}", json=payload)
    data = response.json()
    if not data or "message" not in data:
        raise ValueError("Missing 'server_public_key' in response")
    return data["message"]


def sign_message(message, sign_algorithm, private_key, signature_bytes, timings):
    signature = ctypes.create_string_buffer(signature_bytes)
    sig_len = ctypes.c_size_t()
    start_time = time.time_ns()
    result = sign_algorithm(
        signature, ctypes.byref(sig_len), message, len(message), private_key
    )
    if result != 0:
        raise ValueError("Signing failed")
    timings["sign_time"] = time.time_ns() - start_time
    return signature.raw[: sig_len.value]
