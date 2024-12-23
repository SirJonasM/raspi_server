import ctypes

# Just add signature algorithms here
dilithium2_lib = ctypes.CDLL("./build/crypto_sign/libdilithium2.so")
dilithium3_lib = ctypes.CDLL("./build/crypto_sign/libdilithium3.so")
dilithium5_lib = ctypes.CDLL("./build/crypto_sign/libdilithium5.so")
falcon_512_lib = ctypes.CDLL("./build/crypto_sign/libfalcon-512.so")
falcon_1024_lib = ctypes.CDLL("./build/crypto_sign/libfalcon-1024.so")
rainbowIclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowI-classic.so")
rainbowIIIclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowIII-classic.so")
rainbowVclassic_lib = ctypes.CDLL("./build/crypto_sign/librainbowV-classic.so")


# Add case for new signature algorithms
def get_sign_signature(name):
    match name:
        case "dilithium2":
            return dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature
        case "dilithium3":
            return dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature
        case "dilithium5":
            return dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature
        case "falcon512":
            return falcon_512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_signature
        case "falcon1024":
            return falcon_1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_signature
        case "rainbowIclassic":
            return (
                rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_signature
            )
        case "rainbowIIIclassic":
            return (
                rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_signature
            )
        case "rainbowVclassic":
            return (
                rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_signature
            )
        case _:
            return dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature


# Add case for new signature algorithms:
def get_sign_keypair(name):
    match name:
        case "dilithium2":
            return dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair
        case "dilithium3":
            return dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair
        case "dilithium5":
            return dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair
        case "falcon512":
            return falcon_512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair
        case "falcon1024":
            return falcon_1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair
        case "rainbowIclassic":
            return rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_keypair
        case "rainbowIIIclassic":
            return (
                rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_keypair
            )
        case "rainbowVclassic":
            return rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_keypair
        case _:
            return dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair


def generate_keypair(public_key_size, secret_key_size, algo, name):
    import time

    t = time.time()
    pk = ctypes.create_string_buffer(public_key_size)
    sk = ctypes.create_string_buffer(secret_key_size)
    result = algo(pk, sk)
    if result != 0:
        raise ValueError("Key generation failed")
    print("Key generation time " + name + ": " + str(time.time() - t))
    return (pk.raw, sk.raw)


SIGNATURE_ALGORITHMS = {
    "dilithium2": {
        "public_key_size": 1312,
        "private_key_size": 2528,
        "signature_bytes": 2420,
    },
    "dilithium3": {
        "public_key_size": 1952,
        "private_key_size": 4000,
        "signature_bytes": 3293,
    },
    "dilithium5": {
        "public_key_size": 2592,
        "private_key_size": 4864,
        "signature_bytes": 4595,
    },
    "falcon512": {
        "public_key_size": 897,
        "private_key_size": 1281,
        "signature_bytes": 690,
    },
    "falcon1024": {
        "public_key_size": 1793,
        "private_key_size": 2305,
        "signature_bytes": 1330,
    },
    "rainbowIclassic": {
        "public_key_size": 161600,
        "private_key_size": 103648,
        "signature_bytes": 66,
    },
    "rainbowIIIclassic": {
        "public_key_size": 882080,
        "private_key_size": 626048,
        "signature_bytes": 164,
    },
    "rainbowVclassic": {
        "public_key_size": 1930600,
        "private_key_size": 1408736,
        "signature_bytes": 2420,
    },
}

sign_algorithms = {}


def initialize_keys():
    global sign_algorithms
    for name, sizes in SIGNATURE_ALGORITHMS.items():
        public_key, private_key = generate_keypair(
            sizes["public_key_size"],
            sizes["private_key_size"],
            get_sign_keypair(name),
            name,
        )
        sign_algorithms[name] = {
            "sign_algorithm": get_sign_signature(name),
            "public_key": public_key,
            "private_key": private_key,
            "sign_bytes": sizes["signature_bytes"],
        }
