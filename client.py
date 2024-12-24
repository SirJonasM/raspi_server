from libs_client import KEM_ALGORITHMS, SIGNATURE_ALGORITHMS
from utils_client import send_data
from scheduler import start_scheduler


def run():
    for kem_algorithm in KEM_ALGORITHMS.values():
        for sign_algorithm in SIGNATURE_ALGORITHMS.values():
            try:
                send_data(
                    kem_algorithm["kem_algorithm_name"],
                    kem_algorithm["kem_algorithm"],
                    kem_algorithm["kem_cipher_text_bytes"],
                    kem_algorithm["shared_secret_bytes"],
                    sign_algorithm["sign_algorithm_name"],
                    sign_algorithm["signature_algorithm"],
                    sign_algorithm["sign_public_key"],
                    sign_algorithm["sign_private_key"],
                    sign_algorithm["signature_bytes"],
                )
            except Exception as e:
                print("Error with", kem_algorithm["kem_algorithm_name"], str(e))
                return False
    return True


def test():
    kem_algorithm = KEM_ALGORITHMS["kyber768"]
    sign_algorithm = SIGNATURE_ALGORITHMS["dilithium2"]
    send_data(
        kem_algorithm["kem_algorithm_name"],
        kem_algorithm["kem_algorithm"],
        kem_algorithm["kem_cipher_text_bytes"],
        kem_algorithm["shared_secret_bytes"],
        sign_algorithm["sign_algorithm_name"],
        sign_algorithm["signature_algorithm"],
        sign_algorithm["sign_public_key"],
        sign_algorithm["sign_private_key"],
        sign_algorithm["signature_bytes"],
    )


if __name__ == "__main__":
    start_scheduler()
    i = 0
    while run() and  i < 10_000:
        i+=1
