from flask import Flask, jsonify, request
from utils_server import get_kem_key, handle_client_message
import csv
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    """
    Endpoint to handle client messages. Receives encrypted data, processes it, and returns the response.

    Expects:
        JSON payload with the required fields for `handle_client_message`.

    Returns:
        Flask JSON response: The processed response or an error message.
        HTTP status code: 200 on success, 500 on error.
    """
    data = request.json
    if data is None:
        return jsonify({"message": "Error"}), 500
    try:
        response, status = handle_client_message(**data)
        return jsonify(response), status
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error"}), 500


@app.route("/keys", methods=["POST"])
def get_key():
    """
    Endpoint to retrieve the server's public key for a specified KEM algorithm.

    Expects:
        JSON payload with the field:
            - "kem_name" (str): Name of the KEM algorithm.

    Returns:
        Flask JSON response: The public key in hexadecimal format.
        HTTP status code: 200 on success, 500 on error.
    """
    data = request.json
    if data is None:
        return jsonify({"message": "Error"}), 500
    kem_name = data["kem_name"]
    return get_kem_key(kem_name)


def check_and_write_csv(file_name, header):
    """
    Checks if a CSV file exists. If not, creates it with the specified header.

    Args:
        file_name (str): The name of the CSV file.
        header (list of str): List of column headers for the CSV file.
    """
    if not os.path.exists(file_name):
        print(f"Writing to file: {file_name}")
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)


def file_setup():
    """
    Sets up necessary CSV files for logging key generation and server timings.

    Creates the following files if they do not already exist:
        - "key_generation_times.csv" with columns: "name", "Key Generation Time", "Device Name"
        - "server_timings.csv" with columns: 
            "KEM Algorithm", "Signature Algorithm", "Server Hash Time", 
            "Verify Time", "Decapsulation Time", "Decrypt Time", 
            "Device Name", "Encrypted Data Size"
    """
    check_and_write_csv(
        "server_timings.csv",
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

# Initialize required files on server startup
file_setup()

if __name__ == "__main__":
    """
    Entry point for the Flask application. Starts the server on host 0.0.0.0 and port 5000.
    Debug mode is disabled for production use.
    """
    app.run(host="0.0.0.0", port=5000, debug=False)

