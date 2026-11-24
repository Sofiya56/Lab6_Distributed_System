
import pytest

from app.services.rsa_service import RsaService


@pytest.fixture
def rsa_service():
    return RsaService()


@pytest.fixture
def rsa_keys(rsa_service):
    return rsa_service.generate_crypto_keys()


def test_encrypt_returns_base64(rsa_service, rsa_keys):
    message = "Hello, RSA!"

    encrypted = rsa_service.encrypt(
        rsa_keys.public_key,
        message
    )

    assert isinstance(encrypted, str)
    assert len(encrypted) > 0


def test_decrypt_returns_original_message(
    rsa_service, rsa_keys
):
    message = "Laboratory Work 6"

    encrypted = rsa_service.encrypt(
        rsa_keys.public_key,
        message
    )

    decrypted = rsa_service.decrypt(
        rsa_keys.private_key,
        encrypted
    )

    assert decrypted == message


def test_encrypt_decrypt_unicode(
    rsa_service, rsa_keys
):
    message = "Привіт! Це лабораторна робота №6."

    encrypted = rsa_service.encrypt(
        rsa_keys.public_key,
        message
    )

    decrypted = rsa_service.decrypt(
        rsa_keys.private_key,
        encrypted
    )

    assert decrypted == message
