import os
from cryptography.fernet import Fernet, InvalidToken

# Load encryption key from environment or generate a new one
_KEY_ENV = 'ENCRYPTION_KEY'
_key = os.getenv(_KEY_ENV)
if not _key:
    # Generate a key and log a warning (in production, persist this key securely)
    _key = Fernet.generate_key().decode()
    print(f"[Warning] Environment variable {_KEY_ENV} not set; using a newly generated key.")

_f = Fernet(_key.encode())

def encrypt(plaintext: str) -> str:
    """
    Encrypt a plaintext string and return URL-safe base64-encoded ciphertext.
    """
    if plaintext is None:
        return None
    token = _f.encrypt(plaintext.encode())
    return token.decode()


def decrypt(token: str) -> str:
    """
    Decrypt a URL-safe base64-encoded ciphertext back to plaintext.
    """
    if token is None:
        return None
    try:
        plaintext = _f.decrypt(token.encode())
        return plaintext.decode()
    except InvalidToken:
        raise ValueError("Failed to decrypt token: invalid or tampered data.")

