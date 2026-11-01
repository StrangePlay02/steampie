import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .exceptions import EncryptionError
from .utils import get_json

PBKDF2_ITERATIONS = 50000
SALT_LENGTH = 8
KEY_SIZE_BYTES = 32
IV_LENGTH = 16

backend = default_backend()


@dataclass
class MaFileData:
    steam_id: str
    username: str
    identity_secret: str
    shared_secret: str


def get_random_salt() -> bytes:
    return base64.b64encode(os.urandom(SALT_LENGTH)).decode("utf-8")


def get_initialization_vector() -> bytes:
    return base64.b64encode(os.urandom(IV_LENGTH)).decode("utf-8")


def get_encryption_key(code: str, salt_b64: str) -> bytes:
    salt = base64.b64decode(salt_b64)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=KEY_SIZE_BYTES,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=backend,
    )

    return kdf.derive(code.encode())


def decrypt_data(code: str, salt_b64: str, iv_b64: str, encrypted_data_b64: str | bytes) -> str | None:
    key = get_encryption_key(code, salt_b64)
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(encrypted_data_b64)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    pad_len = padded_plaintext[-1]

    try:
        return padded_plaintext[:-pad_len].decode()
    except UnicodeDecodeError:
        return None


def has_manifest_file(mafile: Path) -> bool:
    for item in mafile.parent.glob("*"):
        if item.name != "manifest.json":
            continue

        data = get_json(item)

        for entry in data.get("entries", []):
            file_name = entry.get("filename")

            if file_name == mafile.name:
                return True

    return False


def is_mafile_unencrypted(mafile: Path) -> bool:
    content = mafile.read_text()
    return "account_name" in content


def get_encryption_values(manifest: Path, mafile: Path) -> dict | None:
    manifest_data = get_json(manifest)

    for entry in manifest_data["entries"]:
        if entry["filename"] == mafile.name:
            return entry


def get_decrypted_data(mafile: Path, code: str | None) -> Any:
    if not has_manifest_file(mafile):
        raise EncryptionError("maFile is encrypted and no manifest.json was found!")

    if not code:
        raise EncryptionError("No code for maFile decryption was given!")

    manifest_file = mafile.parent / "manifest.json"
    encryption_values = get_encryption_values(manifest_file, mafile)

    if not encryption_values:
        raise EncryptionError(f"No encryption values was found for {mafile.name}")

    salt = encryption_values["encryption_salt"]
    iv = encryption_values["encryption_iv"]

    encrypted_data = mafile.read_bytes()
    decrypted_text = decrypt_data(code, salt, iv, encrypted_data)

    if not decrypted_text:
        raise EncryptionError(f"Error when trying to decrypt maFile using code {code}")

    return json.loads(decrypted_text)


def get_mafile_data(mafile: Path, code: str | None = None) -> MaFileData:
    content = None

    if is_mafile_unencrypted(mafile):
        content = get_json(mafile)
    else:
        content = get_decrypted_data(mafile, code)

    return MaFileData(
        content["Session"]["SteamID"],
        content["account_name"],
        content["identity_secret"],
        content["shared_secret"],
    )
