
import base64
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


@dataclass
class AesKey:
    key: str
    iv: str


class AesService:

    def generate_secret_key(self) -> AesKey:
        key = os.urandom(32)
        iv = os.urandom(16)

        return AesKey(
            key=base64.b64encode(key).decode("utf-8"),
            iv=base64.b64encode(iv).decode("utf-8")
        )

    def encrypt(self, aes_key: AesKey, plain_text: str) -> str:
        key = base64.b64decode(aes_key.key)
        iv = base64.b64decode(aes_key.iv)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(
            plain_text.encode("utf-8")
        ) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv)
        )

        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, aes_key: AesKey, cipher_text: str) -> str:
        key = base64.b64decode(aes_key.key)
        iv = base64.b64decode(aes_key.iv)
        encrypted = base64.b64decode(cipher_text, validate=True)

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv)
        )

        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted) + unpadder.finalize()

        return unpadded_data.decode("utf-8")
