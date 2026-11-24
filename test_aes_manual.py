
from app.services.aes_service import AesService

aes_service = AesService()

# Генерация секретного ключа
aes_key = aes_service.generate_secret_key()

print("AES key generated successfully!")

# Исходное сообщение
message = "Hello! This is Laboratory Work 6."

# Шифрование
encrypted = aes_service.encrypt(aes_key, message)

print("Encrypted message:", encrypted)

# Дешифрование
decrypted = aes_service.decrypt(aes_key, encrypted)

print("Decrypted message:", decrypted)

# Проверка
assert message == decrypted

print("AES test passed!")
