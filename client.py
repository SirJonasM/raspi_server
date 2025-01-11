from libs_client import KEM_ALGORITHMS, SIGNATURE_ALGORITHMS
from utils_client import send_data
from scheduler import start_scheduler
import json
import csv
import time


def write_csv_header():
    """Writes the header to the CSV file if it doesn't already exist."""
    try:
        with open("key_generation_times_client.csv", "x", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["Name", "Time"])
    except FileExistsError:
        # File already exists, no need to write the header
        pass


def get_raw_data():
    with open("data.json", "r") as f:
        return json.dumps(json.load(f)).encode("utf-8")


def run():
    raw_data = get_raw_data()
    for kem_algorithm in KEM_ALGORITHMS.values():
        for sign_algorithm in SIGNATURE_ALGORITHMS.values():
            try:
                send_data(
                    raw_data,
                    kem_algorithm["identifier"],
                    kem_algorithm["encapsulation_algorithm"],
                    kem_algorithm["cipher_text_bytes"],
                    kem_algorithm["shared_secret_bytes"],
                    sign_algorithm["identifier"],
                    sign_algorithm["sign_algorithm"],
                    sign_algorithm["public_key"],
                    sign_algorithm["private_key"],
                    sign_algorithm["signature_bytes"],
                )
            except Exception as e:
                print("Error with", kem_algorithm["identifier"], str(e))
                print("Server Error, maybe Restarting")
                time.sleep(5)


def test():
    raw_data = "This is just some simple Text to test with."
    kem_algorithm = KEM_ALGORITHMS["kyber768"]
    sign_algorithm = SIGNATURE_ALGORITHMS["dilithium2"]
    return_message = send_data(
        raw_data,
        kem_algorithm["name"],
        kem_algorithm["encapsulation_algorithm"],
        kem_algorithm["cipher_text_bytes"],
        kem_algorithm["shared_secret_bytes"],
        sign_algorithm["name"],
        sign_algorithm["signature_algorithm"],
        sign_algorithm["public_key"],
        sign_algorithm["private_key"],
        sign_algorithm["signature_bytes"],
    )
    return raw_data == return_message


if __name__ == "__main__":
    start_scheduler()
    i = 0
    while True:
        run()
