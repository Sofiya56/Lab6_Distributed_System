
from fastapi import FastAPI

from app.routers.crypto_keys import router as crypto_keys_router


app = FastAPI(
    title="Distributed Secure Communication System",
    description="API for RSA and AES encryption",
    version="1.0.0"
)

# Підключення RSA API
app.include_router(
    crypto_keys_router,
    prefix="/api/crypto-keys",
    tags=["RSA Cryptography"]
)


@app.get("/")
def root():
    return {
        "message": "Distributed System API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }
