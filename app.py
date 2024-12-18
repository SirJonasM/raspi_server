from key_manager import initialize_keys
initialize_keys()
from flask import Flask
from scheduler import start_scheduler
from kem_algorithms.kems import *
# Initialize Flask app
app = Flask(__name__)

# Register the Kyber512 blueprint
app.register_blueprint(kyber512_blueprint, url_prefix="/kyber512")
app.register_blueprint(kyber768_blueprint, url_prefix="/kyber768")
app.register_blueprint(kyber1024_blueprint, url_prefix="/kyber1024")
app.register_blueprint(hqc128_blueprint, url_prefix="/hqc128")
app.register_blueprint(hqc192_blueprint, url_prefix="/hqc192")
app.register_blueprint(hqc256_blueprint, url_prefix="/hqc256")
# app.register_blueprint(kyber512_rust_blueprint, url_prefix="/kyber512rust")
# app.register_blueprint(kyber768_rust_blueprint, url_prefix="/kyber768rust")
# app.register_blueprint(kyber1024_rust_blueprint, url_prefix="/kyber1024rust")

# Start the scheduler
start_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
