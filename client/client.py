
import requests
import uuid
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from app.services.rsa_service import RsaService
from app.services.aes_service import AesService

BASE_URL = "http://127.0.0.1:8000"

rsa_service = RsaService()
aes_service = AesService()


def get_rsa_public_key(rsa_id):
    response = requests.get(
        f"{BASE_URL}/api/crypto-keys/rsa-public-key/{rsa_id}"
    )
    response.raise_for_status()
    return response.json()["public_key"]


def establish_secure_session(rsa_id):
    print("\nGetting RSA public key...")

    public_key = get_rsa_public_key(rsa_id)
    print("RSA public key received!")

    print("\nGenerating AES key and IV...")

    aes_data = aes_service.generate_secret_key()

    aes_key = aes_data.key
    aes_iv = aes_data.iv

    print("AES key and IV generated!")

    print("\nEncrypting AES key using RSA...")

    encrypted_key = rsa_service.encrypt(public_key, aes_key)
    encrypted_iv = rsa_service.encrypt(public_key, aes_iv)

    print("AES key and IV encrypted!")

    session_id = str(uuid.uuid4())

    print("\nSending session data to server...")

    response = requests.post(
        f"{BASE_URL}/api/crypto-keys/establish-session/{rsa_id}",
        json={
            "session_id": session_id,
            "encrypted_key": encrypted_key,
            "encrypted_iv": encrypted_iv
        }
    )
    response.raise_for_status()

    print("Secure session established successfully!")
    print("Session ID:", session_id)

    return session_id, aes_data


def send_message(session_id, aes_key):
    print("\n=== Secure Message Exchange ===")

    message = input("Enter your message: ")

    encrypted_message = aes_service.encrypt(
        aes_key,
        message
    )

    print("\nEncrypted message sent to server.")

    response = requests.post(
        f"{BASE_URL}/api/crypto-keys/session/{session_id}/message",
        json={
            "cipher_text": encrypted_message
        }
    )
    response.raise_for_status()

    encrypted_response = response.json()["cipher_text"]

    decrypted_response = aes_service.decrypt(
        aes_key,
        encrypted_response
    )

    print("\nServer response:")
    print(decrypted_response)


def main():
    print("=== Secure Communication Client ===")

    try:
        rsa_id = int(input("Enter RSA key ID: "))

        session_id, aes_key = establish_secure_session(rsa_id)

        send_message(session_id, aes_key)

    except requests.exceptions.RequestException as error:
        print("\nServer connection error:", error)

    except Exception as error:
        print("\nError:", error)


if __name__ == "__main__":
    main()
