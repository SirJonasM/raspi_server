import ctypes
from lib_manager import *

# Helper function to generate keypair
def generate_keypair(public_key_size, secret_key_size, algo, name):
    import time
    t = time.time()
    pk = ctypes.create_string_buffer(public_key_size)
    sk = ctypes.create_string_buffer(secret_key_size)
    result = algo(pk, sk)  
    if result != 0:
        raise ValueError("Key generation failed")
    print("Key generation time "+ name + ": " + str(time.time() - t))
    return (pk.raw, sk.raw)

KEY_SIZES = {
    "dilithium2": (1312, 2528),
    "dilithium3": (1952, 4000),
    "dilithium5": (2592, 4864),
    "falcon512": (897, 1281),
    "falcon1024": (1793, 2305),
    "rainbowIclassic": (161600, 103648),
    "rainbowIIIclassic": (882080, 626048),
    "rainbowVclassic": (1930600, 1408736),
}
sign_algorithms = {}

def initialize_keys():
    global sign_algorithms
    sign_algorithms = {
        "dilithium2": {
            "sign_algorithm": dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["dilithium2"],dilithium2_lib.PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair, "dilithium2"),
            "sign_bytes": 2420
            },
        "dilithium3": {
            "sign_algorithm": dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["dilithium3"],dilithium3_lib.PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair, "dilithium3" ),
            "sign_bytes": 3293 
            },
        "dilithium5": {
            "sign_algorithm": dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["dilithium5"],dilithium5_lib.PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair, "dilithium5" ),
            "sign_bytes": 4595 
            },
        "falcon512": {
            "sign_algorithm": falcon_512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["falcon512"],falcon_512_lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair, "falcon512" ),
            "sign_bytes": 690 
            },
        "falcon1024": {
            "sign_algorithm": falcon_1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["falcon1024"],falcon_1024_lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair, "falcon1024" ),
            "sign_bytes": 1330 
            },
        "rainbowIclassic": {
            "sign_algorithm": rainbowIclassic_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["rainbowIclassic"],rainbowI_lib.PQCLEAN_RAINBOWICLASSIC_CLEAN_crypto_sign_keypair, "rainbowIclassic" ),
            "sign_bytes": 66 
            },
        "rainbowIIIclassic": {
            "sign_algorithm": rainbowIIIclassic_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["rainbowIIIclassic"],rainbowIII_lib.PQCLEAN_RAINBOWIIICLASSIC_CLEAN_crypto_sign_keypair, "rainbowIIIclassic" ),
            "sign_bytes": 164 
            },
        "rainbowVclassic": {
            "sign_algorithm": rainbowVclassic_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_signature,
            "sign_keys": generate_keypair(*KEY_SIZES["rainbowVclassic"],rainbowV_lib.PQCLEAN_RAINBOWVCLASSIC_CLEAN_crypto_sign_keypair, "rainbowVclassic" ),
            "sign_bytes": 212 
            },
        }

