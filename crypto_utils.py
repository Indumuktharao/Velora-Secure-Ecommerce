from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path(__file__).parent / "secret.key"

def load_or_create_key():
    """Create a demo encryption key once, then reuse it."""
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return key

def encrypt_message(message: bytes) -> bytes:
    return Fernet(load_or_create_key()).encrypt(message)

def decrypt_message(token: bytes) -> bytes:
    return Fernet(load_or_create_key()).decrypt(token)
