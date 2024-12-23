import json
import time
import ctypes
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from flask import jsonify


def hash_message(message):
    t = time.time()
    message = message.encode() if isinstance(message, str) else message
    hash_obj = hashlib.sha3_256()
    hash_obj.update(message)
    t = time.time() - t
    return hash_obj.digest(), t


def read_and_encrypt_file(aes_key, raw_data):
    timings = {}
    start_time = time.time()
    timings["read_file"] = time.time() - start_time
    start_time = time.time()
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(raw_data, AES.block_size))
    iv = cipher.iv
    timings["encrypt_data"] = time.time() - start_time
    return ciphertext, iv, timings


def encapsulate_key(
    client_public_key, encapsulate_algorithm, cipher_text_bytes, shared_secret_bytes
):
    timings = {}
    encapsulated_key = ctypes.create_string_buffer(cipher_text_bytes)
    shared_secret = ctypes.create_string_buffer(shared_secret_bytes)
    start_time = time.time()
    result = encapsulate_algorithm(encapsulated_key, shared_secret, client_public_key)
    timings["encapsulate_key"] = time.time() - start_time
    if result != 0:
        raise ValueError("Encapsulation failed")

    return encapsulated_key.raw, shared_secret.raw, timings


def get_client_public_key(request):
    data = request.json
    if not data or "client_public_key" not in data:
        raise ValueError("Missing 'client_public_key' in request")

    return bytes.fromhex(data["client_public_key"])


def handle(
    client_public_key,
    encapsulation_algorithm,
    cipher_text_bytes,
    shared_secret_bytes,
    sign_algorithm,
    sign_public_key,
    sign_private_key,
    sign_bytes,
):

    encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(
        client_public_key,
        encapsulation_algorithm,
        cipher_text_bytes,
        shared_secret_bytes,
    )
    with open("data.json", "r") as f:
        raw_data = json.dumps(json.load(f)).encode("utf-8")
    ciphertext, iv, encryption_timings = read_and_encrypt_file(
        shared_secret[:32], raw_data
    )
    hashed_ciphertext, hash_time = hash_message(ciphertext)

    signature, sign_time = sign_message(
        hashed_ciphertext, sign_algorithm, sign_private_key, sign_bytes
    )

    return {
        "data": {"cipher_text": ciphertext.hex(), "iv": iv.hex()},
        "signature": signature.hex(),
        "secret_key": encapsulated_key.hex(),
        "sign_pub_key": sign_public_key.hex(),
        "timings": {
            "hash_time": hash_time,
            "sign_time": sign_time,
            **encryption_timings,
            **encapsulation_timings,
        },
    }


def handle_message(
    request,
    kem_algorithm,
    kem_cipher_text_bytes,
    kem_shared_secret_bytes,
    sign_algorithm,
    public_key,
    private_key,
    sign_bytes,
):
    try:
        client_public_key = get_client_public_key(request)
        response = handle(
            client_public_key,
            kem_algorithm,
            kem_cipher_text_bytes,
            kem_shared_secret_bytes,
            sign_algorithm,
            public_key,
            private_key,
            sign_bytes,
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def sign_message(message, sign_algorithm, private_key, signature_bytes):
    signature = ctypes.create_string_buffer(signature_bytes)
    sig_len = ctypes.c_size_t()
    start_time = time.time()
    result = sign_algorithm(
        signature, ctypes.byref(sig_len), message, len(message), private_key
    )
    t = time.time() - start_time
    if result != 0:
        raise ValueError("Signing failed")
    return signature.raw[: sig_len.value], t
