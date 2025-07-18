import datetime
import json
import subprocess

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from dotenv import load_dotenv

load_dotenv()

import os

CURRENT_PATH = os.getcwd()
EXPONENT = os.getenv('EXPONENT')
KEY_SIZE = os.getenv('KEY_SIZE')
METADATA_SIGNATURE = "metadata_signature"
def generate_private_key():
    return rsa.generate_private_key(public_exponent=int(EXPONENT), key_size=int(KEY_SIZE))

def generate_public_key(private_key):
    return private_key.public_key()

def get_private_pem_bytes(private_key):
    pem_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    return pem_bytes.decode("utf-8")

def get_public_pem_bytes(public_key):
    pem_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem_bytes.decode("utf-8")

def mkdir(user: str, parent_folder: str = "keys"):
    key_path = CURRENT_PATH + f"/{parent_folder}/" + user
    if not os.path.exists(key_path):
        subprocess.run(["mkdir", "-p", key_path])
    return key_path

def write_in_pem_file(user: str):
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    str_private_key = get_private_pem_bytes(private_key)
    str_public_key = get_public_pem_bytes(public_key)
    path = mkdir(user)
    with open(f'{path}/{user}_private.pem', 'w') as f:
        f.write(f"{str_private_key}")
    with open(f'{path}/{user}_public.pem', 'w') as f:
        f.write(f"{str_public_key}")

def read_file(file_path: str, extension: str = ".txt", type_read: str = "r") -> str | bytes:
    if not file_path.endswith(extension):
        raise Exception(f"File {file_path} is not a {extension} file.")
    with open(file_path, type_read) as f:
        return f.read()

def read_private_key_file(user: str):
    key_path = CURRENT_PATH + "/keys/" + user
    private_key = read_file(key_path + f"/{user}_private.pem", ".pem", type_read="rb")
    return serialization.load_pem_private_key(private_key, backend=default_backend(), password=None)

def get_hash_value(file_path: str) -> bytes:
    file_content = read_file(file_path, type_read="rb")
    hash_value = hashes.Hash(hashes.SHA256())
    hash_value.update(file_content)
    return hash_value.finalize()

def sign_file(file_path: str, user: str):
    private_key = read_private_key_file(user)
    hash_value = get_hash_value(file_path)
    signature = private_key.sign(hash_value,
                                    padding=padding.PSS(
                                        mgf=padding.MGF1(hashes.SHA256()),
                                        salt_length=padding.PSS.MAX_LENGTH
                                    ),
                                    algorithm=hashes.SHA256()
                                 )
    return signature

def write_signature_safeguard_file(signature: bytes, user, file_path: str):
    signature_safeguard_file = mkdir(user, parent_folder="metadata_signature")
    new_signature_to_save = {"signature": str(signature), "user": user, "timestamp": str(datetime.datetime.now())}
    with open(signature_safeguard_file + f"/{user}_{file_path}.json", "w+") as f:
        json.dump(new_signature_to_save, f, indent=4)

def store_signature_file(signature: bytes, file_path: str, user: str):
    new_file_path = file_path.replace(".txt", ".sig")
    folder_path = mkdir(user, "signatures")
    with open(folder_path + "/" + new_file_path, "wb") as f:
        f.write(signature)

def process_sign_file(file_path: str, user: str):
    signature = sign_file(file_path, user)
    write_signature_safeguard_file(signature, user, file_path)
    store_signature_file(signature, file_path, user)

