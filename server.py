from flask import Flask, jsonify, request
from utils_server import get_kem_key, handle_client_message
import csv

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


def write_csv_header(output_file="timings.csv"):
    """
    Writes the header to the CSV file.

    Parameters:
        output_file (str): Path to the output CSV file.
    """
    # Define the header
    header = [
        "KEM Algorithm",
        "Signature Algorithm",
        "Encapsulation Time",
        "Encryption Time",
        "Client Hash Time",
        "Sign Time",
        "Server Hash Time",
        "Verify Time",
        "Decapsulation Time",
        "Decrypt Time",
    ]

    # Open the CSV file in write mode and write the header
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)


if __name__ == "__main__":
    write_csv_header()
    app.run()
