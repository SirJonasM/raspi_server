from libs_client import KEM_ALGORITHMS, SIGNATURE_ALGORITHMS
from utils_client import send_data
from scheduler import start_scheduler
import json
import csv
import time
import sys


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


def run(url):
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
                    url,
                )
            except Exception as e:
                print("Error with", kem_algorithm["identifier"], str(e))
                print("Server Error, maybe Restarting")
                time.sleep(5)


def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <SERVER_IP> [PORT=5000]")
        return

    server_ip = sys.argv[1]
    port = 5000  # default
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    url = f"http://{server_ip}:{port}/"

    start_scheduler()
    while True:
        run(url)


if __name__ == "__main__":
    main()
