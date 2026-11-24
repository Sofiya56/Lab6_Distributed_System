
import pytest

from app.services.aes_service import AesService


@pytest.fixture
def aes_service():
    return AesService()


@pytest.fixture
def aes_key(aes_service):
    return aes_service.generate_secret_key()


def test_encrypt_returns_base64(aes_service, aes_key):
    message = "Hello, AES!"

    encrypted = aes_service.encrypt(aes_key, message)

    assert isinstance(encrypted, str)
    assert len(encrypted) > 0


def test_decrypt_returns_original_message(aes_service, aes_key):
    message = "Laboratory Work 6"

    encrypted = aes_service.encrypt(aes_key, message)
    decrypted = aes_service.decrypt(aes_key, encrypted)

    assert decrypted == message


def test_encrypt_decrypt_unicode(aes_service, aes_key):
    message = "Привіт! Це лабораторна робота №6."

    encrypted = aes_service.encrypt(aes_key, message)
    decrypted = aes_service.decrypt(aes_key, encrypted)

    assert decrypted == message


def test_different_encryption_for_different_keys(aes_service):
    message = "Secret message"

    key1 = aes_service.generate_secret_key()
    key2 = aes_service.generate_secret_key()

    encrypted = aes_service.encrypt(key1, message)

    with pytest.raises(Exception):
        aes_service.decrypt(key2, encrypted)
