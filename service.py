import os

from cryptography.hazmat.primitives.asymmetric import rsa
from dotenv import load_dotenv

load_dotenv()

EXPONENT = os.getenv('EXPONENT')

def generate_private_key():
    return rsa.generate_private_key(public_exponent=int(EXPONENT), key_size=2048)