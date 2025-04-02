import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash: str, password: str) -> bool:
    return stored_hash == hash_password(password)

# Show all accounts
def show_account_type(account_type):
    for acc in account_type:
        print(f"Accounts: {acc}")