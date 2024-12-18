import ctypes
import json
import time
from flask import Blueprint, jsonify, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from dilithium2 import hash_and_sign  as dilthium2_hash_and_sign
from dilithium3 import hash_and_sign  as dilthium3_hash_and_sign 
from dilithium5 import hash_and_sign  as dilthium5_hash_and_sign 
from falcon_1024 import hash_and_sign as falcon_1024_hash_and_sign
from falcon_512 import hash_and_sign as falcon_512_hash_and_sign
from rainbowI_classic import hash_and_sign as rainbowI_classic_hash_and_sign
from rainbowIII_classic import hash_and_sign as rainbowIII_classic_hash_and_sign
from rainbowV_classic import hash_and_sign as rainbowV_classic_hash_and_sign

# Load the Kyber library
pqclean = ctypes.CDLL('./build/libpqc_kyber512.so')

# Constants
KYBER_PUBLICKEYBYTES = 800
KYBER_SECRETKEYBYTES = 1632
KYBER_CIPHERTEXTBYTES = 768
KYBER_SHAREDSECRETBYTES = 32

# Flask Blueprint
kyber512_rust_blueprint = Blueprint("kyber512rust", __name__)

def read_and_encrypt_file(aes_key, file_path="data.json"):
    timings = {}

    # Step 4: Read data from the JSON file
    start_time = time.time()
    with open(file_path, 'r') as f:
        raw_data = json.dumps(json.load(f)).encode('utf-8')  # Convert JSON to bytes
    timings['read_file'] = time.time() - start_time

    # Encrypt the data using AES-256
    start_time = time.time()
    cipher = AES.new(aes_key, AES.MODE_CBC)  # Using CBC mode
    ciphertext = cipher.encrypt(pad(raw_data, AES.block_size))
    iv = cipher.iv  # Initialization vector
    timings['encrypt_data'] = time.time() - start_time

    return ciphertext, iv, timings

def encapsulate_key(client_public_key):
    timings = {}

    # Step 7: Encapsulate the AES-256 key using client's public key
    start_time = time.time()
    encapsulated_key = ctypes.create_string_buffer(KYBER_CIPHERTEXTBYTES)
    shared_secret = ctypes.create_string_buffer(KYBER_SHAREDSECRETBYTES)
    result = pqclean.encapsulate_key(client_public_key, encapsulated_key, shared_secret)
    if result != 0:
        raise ValueError("Encapsulation failed")
    timings['encapsulate_key'] = time.time() - start_time

    return encapsulated_key.raw, shared_secret.raw, timings

@kyber512_rust_blueprint.route("/dilithium2", methods=["POST"])
def kyber_dilithium2():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)

        signature, signing_timings = dilthium2_hash_and_sign(ciphertext)


        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@kyber512_rust_blueprint.route("/dilithium3", methods=["POST"])
def kyber_dilithium():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
        
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)

        signature, signing_timings = dilthium3_hash_and_sign(ciphertext)

        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/dilithium5", methods=["POST"])
def kyber_dilithium5():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)

        signature, signing_timings = dilthium5_hash_and_sign(ciphertext)


        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/falcon512", methods=["POST"])
def falcon_512():
    try:
        # Parse client public key from request
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)
        
        signature, signing_timings = falcon_512_hash_and_sign(ciphertext)

        # Combine timings

        # Prepare the response
        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/falcon1024", methods=["POST"])
def falcon_1024():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)
        
        signature, signing_timings = falcon_1024_hash_and_sign(ciphertext)

        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/rainbowI", methods=["POST"])
def rainbow_encapsulate():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)
        
        signature, signing_timings = rainbowI_classic_hash_and_sign(ciphertext)

        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/rainbowIII", methods=["POST"])
def kyber_rainbowIII():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)
        
        signature, signing_timings = rainbowIII_classic_hash_and_sign(ciphertext)

        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@kyber512_rust_blueprint.route("/rainbowV", methods=["POST"])
def kyber_rainbowV():
    try:
        data = request.json
        if not data or 'client_public_key' not in data:
            raise ValueError("Missing 'client_public_key' in request")

        client_public_key = bytes.fromhex(data['client_public_key'])

        encapsulated_key, shared_secret, encapsulation_timings = encapsulate_key(client_public_key)
       
        ciphertext, iv, encryption_timings = read_and_encrypt_file(shared_secret)
        
        signature, signing_timings = rainbowV_classic_hash_and_sign(ciphertext)

        response = {
            "data": {
                "cipher_text": ciphertext.hex(),
                "iv": iv.hex()
            },
            "signature": signature.hex(),
            "secret_key": encapsulated_key.hex(),
            "timings": {
                **encryption_timings,
                **signing_timings,
                **encapsulation_timings,
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
