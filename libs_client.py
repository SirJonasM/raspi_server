import ctypes

kyber512rust_lib = ctypes.CDLL("./build/crypto_kem/libkyber512rust.so")
kyber768rust_lib = ctypes.CDLL("./build/crypto_kem/libkyber768rust.so")
kyber1024rust_lib = ctypes.CDLL("./build/crypto_kem/libkyber1024rust.so")
kyber512_lib = ctypes.CDLL("./build/crypto_kem/libkyber512.so")
kyber768_lib = ctypes.CDLL("./build/crypto_kem/libkyber768.so")
kyber1024_lib = ctypes.CDLL("./build/crypto_kem/libkyber1024.so")
hqcrmrs128_lib = ctypes.CDLL("./build/crypto_kem/libhqc-rmrs-128.so")
hqcrmrs192_lib = ctypes.CDLL("./build/crypto_kem/libhqc-rmrs-192.so")
hqcrmrs256_lib = ctypes.CDLL("./build/crypto_kem/libhqc-rmrs-256.so")

dilithium2_lib = ctypes.CDLL("./build/crypto_sign/libdilithium2.so")
dilithium3_lib = ctypes.CDLL("./build/crypto_sign/libdilithium3.so")
dilithium5_lib = ctypes.CDLL("./build/crypto_sign/libdilithium5.so")
falcon512_lib = ctypes.CDLL("./build/crypto_sign/libfalcon-512.so")
falcon1024_lib = ctypes.CDLL("./build/crypto_sign/libfalcon-1024.so")
rainbowIclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowI-classic.so")
rainbowIIIclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowIII-classic.so")
rainbowVclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowV-classic.so")

KEM_ALGORITHMS = {
    "kyber512rust": {
        "identifier": "kyber512rust",
        "encapsulat_algorithm": kyber512rust_lib.encapsulate_key,
        "cipher_text_bytes": 768,
        "shared_secret_bytes": 32,
        "public_key_bytes": 800,
        "private_key_bytes": 1632,
    },
    "kyber768rust": {
        "identifier": "kyber768rust",
        "encapsulat_algorithm": kyber768rust_lib.encapsulate_key,
        "cipher_text_bytes": 1088,
        "shared_secret_bytes": 32,
        "public_key_bytes": 2400,
        "private_key_bytes": 1184,
    },
    "kyber1024rust": {
        "identifier": "kyber1024rust",
        "encapsulat_algorithm": kyber1024rust_lib.encapsulate_key,
        "cipher_text_bytes": 1568,
        "shared_secret_bytes": 32,
        "public_key_bytes": 1568,
        "private_key_bytes": 3168,
    },
    "kyber512": {
        "identifier": "kyber512",
        "encapsulat_algorithm": kyber512_lib.PQCLEAN_KYBER512_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 768,
        "shared_secret_bytes": 32,
        "public_key_bytes": 800,
        "private_key_bytes": 1632,
    },
    "kyber768": {
        "identifier": "kyber768",
        "encapsulat_algorithm": kyber768_lib.PQCLEAN_KYBER768_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 1088,
        "shared_secret_bytes": 32,
        "public_key_bytes": 2400,
        "private_key_bytes": 1184,
    },
    "kyber1024": {
        "identifier": "kyber1024",
        "encapsulat_algorithm": kyber1024_lib.PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 1568,
        "shared_secret_bytes": 32,
        "public_key_bytes": 1568,
        "private_key_bytes": 3168,
    },
    "hqc-rmrs-128": {
        "identifier": "hqc-rmrs-128",
        "encapsulat_algorithm": hqcrmrs128_lib.PQCLEAN_HQCRMRS128_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 4481,
        "shared_secret_bytes": 64,
        "public_key_bytes": 2249,
        "private_key_bytes": 2289,
    },
    "hqc-rmrs-192": {
        "identifier": "hqc-rmrs-192",
        "encapsulat_algorithm": hqcrmrs192_lib.PQCLEAN_HQCRMRS192_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 9026,
        "shared_secret_bytes": 64,
        "public_key_bytes": 4522,
        "private_key_bytes": 4562,
    },
    "hqc-rmrs-256": {
        "identifier": "hqc-rmrs-256",
        "encapsulat_algorithm": hqcrmrs256_lib.PQCLEAN_HQCRMRS256_CLEAN_crypto_kem_enc,
        "cipher_text_bytes": 14469,
        "shared_secret_bytes": 64,
        "public_key_bytes": 2249,
        "private_key_bytes": 7285,
    },
}


def generate_keypair(public_key_size, secret_key_size, algo, name):
    import time

    t = time.time()
    pk = ctypes.create_string_buffer(public_key_size)
    sk = ctypes.create_string_buffer(secret_key_size)
    result = algo(pk, sk)
    if result != 0:
        raise ValueError("Key generation failed")
    print("Key generation time " + name + ": " + str(time.time() - t))
    return {"public_key": pk.raw, "private_key": sk.raw}


SIGNATURE_ALGORITHMS = {
    "dilithium2": {
        "identifier": "dilithium2",
        "public_key_size": 1312,
        "private_key_size": 2528,
        "signature_bytes": 2420,
        **generate_keypair(
            1312,
            2528,
            dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair,
            "dilithium2",
        ),
        "keypair_algorithm": dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair,
        "sign_algorithm": dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature,
    },
    "dilithium3": {
        "identifier": "dilithium3",
        "public_key_size": 1952,
        "private_key_size": 4000,
        "signature_bytes": 3293,
        **generate_keypair(
            1952,
            4000,
            dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair,
            "dilithium3",
        ),
        "keypair_algorithm": dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair,
        "sign_algorithm": dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature,
    },
    "dilithium5": {
        "identifier": "dilithium5",
        "public_key_size": 2592,
        "private_key_size": 4864,
        "signature_bytes": 4595,
        **generate_keypair(
            2592,
            4864,
            dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair,
            "dilithium5",
        ),
        "keypair_algorithm": dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair,
        "sign_algorithm": dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature,
    },
    "falcon512": {
        "identifier": "falcon512",
        "public_key_size": 897,
        "private_key_size": 1281,
        "signature_bytes": 690,
        **generate_keypair(
            897,
            1281,
            falcon512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair,
            "falcon512",
        ),
        "keypair_algorithm": falcon512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair,
        "sign_algorithm": falcon512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_signature,
    },
    "falcon1024": {
        "identifier": "falcon1024",
        "public_key_size": 1793,
        "private_key_size": 2305,
        "signature_bytes": 1330,
        **generate_keypair(
            1793,
            2305,
            falcon1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair,
            "falcon1024",
        ),
        "keypair_algorithm": falcon1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair,
        "sign_algorithm": falcon1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_signature,
    },
    "rainbowIclassic": {
        "identifier": "rainbowIclassic",
        "public_key_size": 161600,
        "private_key_size": 103648,
        "signature_bytes": 66,
        **generate_keypair(
            161600,
            103648,
            rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_keypair,
            "rainbowIclassic",
        ),
        "keypair_algorithm": rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_keypair,
        "sign_algorithm": rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_signature,
    },
    "rainbowIIIclassic": {
        "identifier": "rainbowIIIclassic",
        "public_key_size": 882080,
        "private_key_size": 626048,
        "signature_bytes": 164,
        **generate_keypair(
            882080,
            626048,
            rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_keypair,
            "rainbowIIIclassic",
        ),
        "keypair_algorithm": rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_keypair,
        "sign_algorithm": rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_signature,
    },
    "rainbowVclassic": {
        "identifier": "rainbowVclassic",
        "public_key_size": 1930600,
        "private_key_size": 1408736,
        "signature_bytes": 212,
        **generate_keypair(
            1930600,
            1408736,
            rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_keypair,
            "rainbowVclassic",
        ),
        "keypair_algorithm": rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_keypair,
        "sign_algorithm": rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_signature,
    },
}
