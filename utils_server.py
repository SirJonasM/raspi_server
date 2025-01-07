import time
import ctypes
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from flask import jsonify
from libs_server import SIGNATURE_ALGORITHMS, KEM_ALGORITHMS
import csv


def hash_message(message, timings):
    t = time.time_ns()
    message = message.encode() if isinstance(message, str) else message
    hash_obj = hashlib.sha3_256()
    hash_obj.update(message)
    timings["server_hash_time"] = time.time_ns() - t
    return hash_obj.digest()


def verify_signature(
    sign_algorithm_name, cipher_text, signature, sign_pub_key, timings
):
    hashed_cipher_text = hash_message(cipher_text, timings)
    verify_signature_algo = SIGNATURE_ALGORITHMS[sign_algorithm_name][
        "verify_algorithm"
    ]

    sig_ptr = (ctypes.c_uint8 * len(signature)).from_buffer_copy(signature)
    sig_len = ctypes.c_size_t(len(signature))

    msg_ptr = (ctypes.c_uint8 * len(hashed_cipher_text)).from_buffer_copy(
        hashed_cipher_text
    )
    msg_len = ctypes.c_size_t(len(hashed_cipher_text))

    pk_ptr = (ctypes.c_uint8 * len(sign_pub_key)).from_buffer_copy(sign_pub_key)

    start_time = time.time_ns()

    result = verify_signature_algo(
        sig_ptr,
        sig_len,
        msg_ptr,
        msg_len,
        pk_ptr,
    )

    timings["verify_time"] = time.time_ns() - start_time
    return result == 0


def decrypt_message(aes_key, iv, cipher_text, timings):
    start_time = time.time_ns()
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    message = unpad(cipher.decrypt(cipher_text), AES.block_size)
    timings["decrypt_time"] = time.time_ns() - start_time
    return message.decode("utf-8")


def decapsulate_aes_key(secret_key_encrypted, kem_algo_name, timings):
    kem_algo_info = KEM_ALGORITHMS[kem_algo_name]
    kem_private_key = kem_algo_info["private_key"]
    kem_algo = kem_algo_info["decapsulation_algorithm"]
    kem_algo_secret_bytes = kem_algo_info["shared_secret_bytes"]
    ss_buffer = ctypes.create_string_buffer(kem_algo_secret_bytes)

    ct_ptr = (ctypes.c_uint8 * len(secret_key_encrypted)).from_buffer_copy(
        secret_key_encrypted
    )
    sk_ptr = (ctypes.c_uint8 * len(kem_private_key)).from_buffer_copy(kem_private_key)

    start_time = time.time_ns()

    result = kem_algo(ss_buffer, ct_ptr, sk_ptr)

    timings["decapsulation_time"] = time.time_ns() - start_time

    if result != 0:
        raise ValueError(f"Decapsulation failed with error code {result}")

    return ss_buffer.raw


def match_data_with_raw_data(data):
    pass


def write_timings_to_file(
    timings, kem_algo_name, sign_algorithm_name, output_file="timings.csv"
):
    # Prepare the data row with algorithm names and timings
    data_row = [kem_algo_name, sign_algorithm_name] + list(timings.values())

    # Open the CSV file in append mode
    with open(output_file, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_row)


def handle_client_message(
    cipher_text,
    iv,
    signature,
    secret_key,
    sign_pub_key,
    timings,
    kem_algo_name,
    sign_algorithm_name,
):
    signature_bytes = bytes.fromhex(signature)
    sign_pub_key_bytes = bytes.fromhex(sign_pub_key)
    cipher_text_bytes = bytes.fromhex(cipher_text)
    secret_key_bytes = bytes.fromhex(secret_key)
    iv_bytes = bytes.fromhex(iv)

    if not verify_signature(
        sign_algorithm_name,
        cipher_text_bytes,
        signature_bytes,
        sign_pub_key_bytes,
        timings,
    ):
        return {"message": "Could not verify signature."}, 500

    aes_key = decapsulate_aes_key(secret_key_bytes, kem_algo_name, timings)

    message = decrypt_message(aes_key[:32], iv_bytes, cipher_text_bytes, timings)

    write_timings_to_file(timings, kem_algo_name, sign_algorithm_name)

    return {"message": message}, 200


def get_kem_key(kem_name):
    key = KEM_ALGORITHMS[kem_name]["public_key"]

    return jsonify({"server_public_key": key.hex()})
