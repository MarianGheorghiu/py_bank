import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash: str, password: str) -> bool:
    return stored_hash == hash_password(password)