
# Розподілена система захищеного зв'язку

## Опис проєкту

Проєкт реалізує розподілену систему для встановлення захищеного каналу зв'язку між клієнтом і сервером.

Система використовує:
- RSA-2048 для безпечного обміну ключами AES.
- AES-256-CBC для шифрування повідомлень.
- FastAPI для створення REST API.
- Зберігання ключів і сесій у пам'яті.

## Використані технології

- Python 3.13
- FastAPI
- Cryptography
- Requests
- Pytest

## Встановлення

Створення віртуального середовища:

```bash
python -m venv venv
```

Активація середовища у Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Встановлення залежностей:

```bash
pip install -r requirements.txt
```

## Запуск сервера

```bash
python -m uvicorn app.main:app --reload
```

Документація Swagger: http://127.0.0.1:8000/docs

## Запуск клієнта

```bash
python client/client.py
```

## Запуск тестів

```bash
pytest -v
```

## Запуск через Docker

```bash
docker build -t secure-communication-system .
docker run -p 8000:8000 secure-communication-system
```

## Алгоритм роботи системи

1. Клієнт отримує відкритий RSA-ключ сервера.
2. Клієнт генерує AES-ключ та IV.
3. Клієнт шифрує AES-ключ та IV за допомогою RSA.
4. Сервер розшифровує ключі та створює захищену сесію.
5. Клієнт і сервер обмінюються зашифрованими повідомленнями за допомогою AES.
 