import ctypes
from flask import Blueprint, request
from utils import handle_message
from key_manager import sign_algorithms

name = "hqc-rmrs-192"
PUBLICKEYBYTES = 4522
SECRETKEYBYTES = 4562
CIPHERTEXTBYTES = 9026
SHAREDSECRETBYTES = 64

pqclean = ctypes.CDLL('./build/crypto_kem/lib' + name + '.so')
ALGORITHM = pqclean.PQCLEAN_HQCRMRS192_CLEAN_crypto_kem_enc

blueprint = Blueprint(name, __name__)

@blueprint.route("/dilithium2", methods=["POST"])
def dilithium2():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["dilithium2"])

@blueprint.route("/dilithium3", methods=["POST"])
def dilithium3():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["dilithium3"])


@blueprint.route("/dilithium5", methods=["POST"])
def dilithium5():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["dilithium5"])


@blueprint.route("/falcon512", methods=["POST"])
def falcon512():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["falcon512"])


@blueprint.route("/falcon1024", methods=["POST"])
def falcon1024():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["falcon1024"])


@blueprint.route("/rainbowI", methods=["POST"])
def rainbowI():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["rainbowIclassic"])


@blueprint.route("/rainbowIII", methods=["POST"])
def rainbowIII():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["rainbowIIIclassic"])


@blueprint.route("/rainbowV", methods=["POST"])
def kyber_rainbowV():
    return handle_message(request, ALGORITHM, CIPHERTEXTBYTES, SHAREDSECRETBYTES, **sign_algorithms["rainbowVclassic"])
