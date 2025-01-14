from flask import Flask, jsonify, request
from utils_server import get_kem_key, handle_client_message
import csv
import os

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    data = request.json
    if data is None:
        return jsonify({"message": "Error"})
    response, status = handle_client_message(**data)
    return jsonify(response), status


@app.route("/keys", methods=["POST"])
def get_key():
    data = request.json
    if data is None:
        return jsonify({"message": "Error"}), 500
    kem_name = data["kem_name"]
    return get_kem_key(kem_name)


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
            "Server Hash Time",
            "Verify Time",
            "Decapsulation Time",
            "Decrypt Time",
            "Device Name",
            "Encrypted Data Size",
        ],
    )
    with open("key_sizes_server.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "public_key_size", "secret_key_size"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
