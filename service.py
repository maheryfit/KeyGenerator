import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from dotenv import load_dotenv

load_dotenv()

EXPONENT = os.getenv('EXPONENT')
KEY_SIZE = os.getenv('KEY_SIZE')

def generate_private_key():
    return rsa.generate_private_key(public_exponent=int(EXPONENT), key_size=int(KEY_SIZE))

def generate_public_key(private_key):
    return private_key.public_key()

def get_private_pem_bytes(private_key):
    pem_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    return pem_bytes.decode("utf-8")

def get_public_pem_bytes(public_key):
    pem_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1)
    return pem_bytes.decode("utf-8")

def write_in_pem_file(user: str):
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    str_private_key = get_private_pem_bytes(private_key)
    str_public_key = get_public_pem_bytes(public_key)
    with open(f'{user}_private.pem', 'w') as f:
        f.write(f"{str_private_key}")
    with open(f'{user}_public.pem', 'w') as f:
        f.write(f"{str_public_key}")