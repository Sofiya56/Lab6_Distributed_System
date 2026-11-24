
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from itertools import count
from datetime import datetime, timezone
import base64

from app.services.rsa_service import RsaService
from app.services.aes_service import AesService, AesKey

router = APIRouter()

rsa_service = RsaService()
aes_service = AesService()

rsa_keys_storage = {}
aes_keys_storage = {}
sessions_storage = {}

rsa_id_counter = count(1)
aes_id_counter = count(1)


class EncryptRequest(BaseModel):
    message: str


class DecryptRequest(BaseModel):
    cipher_text: str


class SessionKeyRequest(BaseModel):
    session_id: str
    encrypted_key: str
    encrypted_iv: str


class SessionMessageRequest(BaseModel):
    cipher_text: str


# Generate RSA key pair
@router.post("/generate/rsa-keys")
def generate_rsa_keys():
    try:
        keys = rsa_service.generate_crypto_keys()
        key_id = next(rsa_id_counter)
        rsa_keys_storage[key_id] = keys

        return {
            "id": key_id,
            "message": "RSA keys generated successfully"
        }
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


# Get RSA public key
@router.get("/rsa-public-key/{id}")
def get_rsa_public_key(id: int):
    keys = rsa_keys_storage.get(id)

    if keys is None:
        raise HTTPException(status_code=404, detail="RSA key pair not found")

    return {"public_key": keys.public_key}


# Generate AES key
@router.post("/generate/aes-key")
def generate_aes_key():
    try:
        aes_key = aes_service.generate_secret_key()
        key_id = next(aes_id_counter)
        aes_keys_storage[key_id] = aes_key

        return {
            "id": key_id,
            "message": "AES key generated successfully"
        }
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


# AES encrypt
@router.post("/aes/encrypt/{id}")
def encrypt_message(id: int, request: EncryptRequest):
    aes_key = aes_keys_storage.get(id)

    if aes_key is None:
        raise HTTPException(status_code=404, detail="AES key not found")

    try:
        return {
            "cipher_text": aes_service.encrypt(aes_key, request.message)
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Encryption failed")


# AES decrypt
@router.post("/aes/decrypt/{id}")
def decrypt_message(id: int, request: DecryptRequest):
    aes_key = aes_keys_storage.get(id)

    if aes_key is None:
        raise HTTPException(status_code=404, detail="AES key not found")

    try:
        return {
            "message": aes_service.decrypt(aes_key, request.cipher_text)
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed")


# Establish secure session
@router.post("/establish-session/{rsa_id}")
def establish_session(rsa_id: int, request: SessionKeyRequest):
    rsa_keys = rsa_keys_storage.get(rsa_id)

    if rsa_keys is None:
        raise HTTPException(status_code=404, detail="RSA key pair not found")

    try:
        aes_key = rsa_service.decrypt(
            rsa_keys.private_key,
            request.encrypted_key
        )
        aes_iv = rsa_service.decrypt(
            rsa_keys.private_key,
            request.encrypted_iv
        )

        key_bytes = base64.b64decode(aes_key, validate=True)
        iv_bytes = base64.b64decode(aes_iv, validate=True)

        if len(key_bytes) != 32 or len(iv_bytes) != 16:
            raise ValueError("Invalid AES key or IV")

        sessions_storage[request.session_id] = AesKey(
            key=aes_key,
            iv=aes_iv
        )

        return {
            "message": "Secure session established successfully",
            "session_id": request.session_id
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Session key decryption failed"
        )


# Receive encrypted message and return encrypted response
@router.post("/session/{session_id}/message")
def exchange_message(
    session_id: str,
    request: SessionMessageRequest
):
    aes_key = sessions_storage.get(session_id)

    if aes_key is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    try:
        decrypted_message = aes_service.decrypt(
            aes_key,
            request.cipher_text
        )

        received_at = datetime.now(timezone.utc).isoformat()

        response_message = (
            f"Server received: {decrypted_message}. "
            f"Received at: {received_at}"
        )

        encrypted_response = aes_service.encrypt(
            aes_key,
            response_message
        )

        return {
            "cipher_text": encrypted_response
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Message processing failed"
        )
