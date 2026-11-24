
import base64
from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


@dataclass
class RsaKeys:
    public_key: str
    private_key: str


class RsaService:

    def generate_crypto_keys(self) -> RsaKeys:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return RsaKeys(
            public_key=base64.b64encode(public_pem).decode("utf-8"),
            private_key=base64.b64encode(private_pem).decode("utf-8")
        )

    def encrypt(self, public_key: str, plain_text: str) -> str:
        public_pem = base64.b64decode(public_key)

        key = serialization.load_pem_public_key(public_pem)

        encrypted = key.encrypt(
            plain_text.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, private_key: str, cipher_text: str) -> str:
        private_pem = base64.b64decode(private_key)

        key = serialization.load_pem_private_key(
            private_pem,
            password=None
        )

        encrypted = base64.b64decode(cipher_text, validate=True)

        decrypted = key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted.decode("utf-8")
