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
# int PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(uint8_t *ss, const uint8_t *ct, const uint8_t *sk);
# int PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(uint8_t *pk, uint8_t *sk);


def generate_keypair(public_key_size, secret_key_size, algo, name):
    import time

    t = time.time()
    pk = ctypes.create_string_buffer(public_key_size)
    sk = ctypes.create_string_buffer(secret_key_size)
    result = algo(pk, sk)
    if result != 0:
        raise ValueError("Key generation failed")
    print("Key generation time " + name + ": " + str(time.time() - t))
    return {"kem_public_key": pk.raw, "kem_private_key": sk.raw}


KEM_ALGORITHMS = {
    "kyber512rust": {
        "kem_algorithm_name": "kyber512rust",
        "kem_algorithm": kyber512rust_lib.decapsulate_key,
        "kem_key_pair": kyber512rust_lib.generate_keypair,
        **generate_keypair(
            800, 1632, kyber512rust_lib.generate_keypair, "kyber512rust"
        ),
        "kem_cipher_text_bytes": 768,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 800,
        "kem_private_key_bytes": 1632,
    },
    "kyber768rust": {
        "kem_algorithm_name": "kyber768rust",
        "kem_algorithm": kyber768rust_lib.decapsulate_key,
        "kem_key_pair": kyber768rust_lib.generate_keypair,
        **generate_keypair(
            1184, 2400, kyber768rust_lib.generate_keypair, "kyber768rust"
        ),
        "kem_cipher_text_bytes": 1088,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 2400,
        "kem_private_key_bytes": 1184,
    },
    "kyber1024rust": {
        "kem_algorithm_name": "kyber1024rust",
        "kem_algorithm": kyber1024rust_lib.decapsulate_key,
        "kem_key_pair": kyber1024rust_lib.generate_keypair,
        **generate_keypair(
            1568, 3168, kyber1024rust_lib.generate_keypair, "kyber1024rust"
        ),
        "kem_cipher_text_bytes": 1568,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 1568,
        "kem_private_key_bytes": 3168,
    },
    "kyber512": {
        "kem_algorithm_name": "kyber512",
        "kem_algorithm": kyber512_lib.PQCLEAN_KYBER512_CLEAN_crypto_kem_dec,
        "kem_key_pair": kyber512_lib.PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            800,
            1632,
            kyber512_lib.PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair,
            "kyber512",
        ),
        "kem_cipher_text_bytes": 768,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 800,
        "kem_private_key_bytes": 1632,
    },
    "kyber768": {
        "kem_algorithm_name": "kyber768",
        "kem_algorithm": kyber768_lib.PQCLEAN_KYBER768_CLEAN_crypto_kem_dec,
        "kem_key_pair": kyber768_lib.PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            1184,
            2400,
            kyber768_lib.PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair,
            "kyber768",
        ),
        "kem_cipher_text_bytes": 1088,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 1184,
        "kem_private_key_bytes": 2400,
    },
    "kyber1024": {
        "kem_algorithm_name": "kyber1024",
        "kem_algorithm": kyber1024_lib.PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec,
        "kem_key_pair": kyber1024_lib.PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            1568,
            3168,
            kyber1024_lib.PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair,
            "kyber1024",
        ),
        "kem_cipher_text_bytes": 1568,
        "shared_secret_bytes": 32,
        "kem_public_key_bytes": 1568,
        "kem_private_key_bytes": 3168,
    },
    "hqc-rmrs-128": {
        "kem_algorithm_name": "hqc-rmrs-128",
        "kem_algorithm": hqcrmrs128_lib.PQCLEAN_HQCRMRS128_CLEAN_crypto_kem_dec,
        "kem_key_pair": hqcrmrs128_lib.PQCLEAN_HQCRMRS128_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            2249,
            2289,
            hqcrmrs128_lib.PQCLEAN_HQCRMRS128_CLEAN_crypto_kem_keypair,
            "hqc-rmrs-128",
        ),
        "kem_cipher_text_bytes": 4481,
        "shared_secret_bytes": 64,
        "kem_public_key_bytes": 2249,
        "kem_private_key_bytes": 2289,
    },
    "hqc-rmrs-192": {
        "kem_algorithm_name": "hqc-rmrs-192",
        "kem_algorithm": hqcrmrs192_lib.PQCLEAN_HQCRMRS192_CLEAN_crypto_kem_dec,
        "kem_key_pair": hqcrmrs192_lib.PQCLEAN_HQCRMRS192_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            4522,
            4562,
            hqcrmrs192_lib.PQCLEAN_HQCRMRS192_CLEAN_crypto_kem_keypair,
            "hqc-rmrs-192",
        ),
        "kem_cipher_text_bytes": 9026,
        "shared_secret_bytes": 64,
        "kem_public_key_bytes": 4522,
        "kem_private_key_bytes": 4562,
    },
    "hqc-rmrs-256": {
        "kem_algorithm_name": "hqc-rmrs-256",
        "kem_algorithm": hqcrmrs256_lib.PQCLEAN_HQCRMRS256_CLEAN_crypto_kem_dec,
        "kem_key_pair": hqcrmrs256_lib.PQCLEAN_HQCRMRS256_CLEAN_crypto_kem_keypair,
        **generate_keypair(
            7245,
            7285,
            hqcrmrs256_lib.PQCLEAN_HQCRMRS256_CLEAN_crypto_kem_keypair,
            "hqc-rmrs-256",
        ),
        "kem_cipher_text_bytes": 14469,
        "shared_secret_bytes": 64,
        "kem_public_key_bytes": 7245,
        "kem_private_key_bytes": 7285,
    },
}


# int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify(
#    const uint8_t *sig, size_t siglen,
#    const uint8_t *m, size_t mlen, const uint8_t *pk);

SIGNATURE_ALGORITHMS = {
    "dilithium2": {
        "sign_algorithm_name": "dilithium2",
        "public_key_size": 1312,
        "private_key_size": 2528,
        "signature_bytes": 2420,
        "verify_algorithm": dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify,
    },
    "dilithium3": {
        "sign_algorithm_name": "dilithium3",
        "public_key_size": 1952,
        "private_key_size": 4000,
        "signature_bytes": 3293,
        "verify_algorithm": dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_verify,
    },
    "dilithium5": {
        "sign_algorithm_name": "dilithium5",
        "public_key_size": 2592,
        "private_key_size": 4864,
        "signature_bytes": 4595,
        "verify_algorithm": dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_verify,
    },
    "falcon512": {
        "sign_algorithm_name": "falcon512",
        "public_key_size": 897,
        "private_key_size": 1281,
        "signature_bytes": 690,
        "verify_algorithm": falcon512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_verify,
    },
    "falcon1024": {
        "sign_algorithm_name": "falcon1024",
        "public_key_size": 1793,
        "private_key_size": 2305,
        "signature_bytes": 1330,
        "verify_algorithm": falcon1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_verify,
    },
    "rainbowIclassic": {
        "sign_algorithm_name": "rainbowIclassic",
        "public_key_size": 161600,
        "private_key_size": 103648,
        "signature_bytes": 66,
        "verify_algorithm": rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_verify,
    },
    "rainbowIIIclassic": {
        "sign_algorithm_name": "rainbowIIIclassic",
        "public_key_size": 882080,
        "private_key_size": 626048,
        "signature_bytes": 164,
        "verify_algorithm": rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_verify,
    },
    "rainbowVclassic": {
        "sign_algorithm_name": "rainbowVclassic",
        "public_key_size": 1930600,
        "private_key_size": 1408736,
        "signature_bytes": 212,
        "verify_algorithm": rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_verify,
    },
}
