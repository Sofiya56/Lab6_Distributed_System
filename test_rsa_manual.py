
from app.services.rsa_service import RsaService

rsa_service = RsaService()

# Генерация ключей
keys = rsa_service.generate_crypto_keys()

print("RSA keys generated successfully!")

# Исходное сообщение
message = "Hello! This is Laboratory Work 6."

# Шифрование
encrypted = rsa_service.encrypt(
    keys.public_key,
    message
)

print("Encrypted message:", encrypted)

# Дешифрование
decrypted = rsa_service.decrypt(
    keys.private_key,
    encrypted
)

print("Decrypted message:", decrypted)

# Проверка
assert message == decrypted

print("RSA test passed!")
