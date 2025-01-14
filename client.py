from libs_client import KEM_ALGORITHMS, SIGNATURE_ALGORITHMS
from utils_client import send_data
import csv
import time
import sys
import requests
import os

url = "https://ogcapi.hft-stuttgart.de/sta/udigit4icity/v1.1/Observations"

CLIENT_DEVICE = os.getenv("DEVICE_NAME")


def fetch():
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Ensure UTF-8 decoding
        text_data = response.text
        return text_data

    except Exception as e:
        print(f"Error fetching data: {e}")


RAW_DATA = fetch()


def check_and_write_csv(file_name, header):
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)


def file_setup():
    check_and_write_csv(
        "key_generation_times.csv", ["name", "Key Generation Time", "Device Name"]
    )
    check_and_write_csv(
        "timings_client.csv",
        [
            "KEM Algorithm",
            "Signature Algorithm",
            "Client Device",
            "Encapsulation Time",
            "Encryption Time",
            "Client Hash Time",
            "Sign Time",
            "Data Size",
        ],
    )
    with open("key_sizes_client.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "public_key_size", "secret_key_size"])


def write_timings(timings, kem_algorithm, sign_algorithm):
    with open("timings_client", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                kem_algorithm,
                sign_algorithm,
                CLIENT_DEVICE,
                timings["encapsulation_time"],
                timings["encryption_time"],
                timings["client_hash_time", "sign_time", RAW_DATA],
            ]
        )


def run(url):
    for kem_algorithm in KEM_ALGORITHMS.values():
        for sign_algorithm in SIGNATURE_ALGORITHMS.values():
            try:
                _message, timings = send_data(
                    RAW_DATA,
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
                write_timings(timings, kem_algorithm, sign_algorithm)
            except Exception as e:
                print("Error with", kem_algorithm["identifier"], str(e))
                print("Server Error, maybe Restarting")
                time.sleep(5)


def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <SERVER_IP> [PORT=5000]")
        return

    server_ip = sys.argv[1]
    port = 5000
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    url = f"http://{server_ip}:{port}/"

    while True:
        run(url)


if __name__ == "__main__":
    main()
