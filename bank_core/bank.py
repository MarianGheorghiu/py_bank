from config import db_path
import json
import os

class Bank:
    def __init__(self, accounts_file=db_path):
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()
        
    def load_accounts(self):
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                return json.load(f)
        return []
    
    def save_accounts(self):
        with open(self.accounts_file, "w") as f:
            json.dump(self.accounts, f, indent=4)
    
    def create_account(self, first_name, last_name, account_number, account_id, balance=0):
        new_account = {
            "first_name": first_name,
            "last_name": last_name,
            "account_number": account_number,
            "account_id": account_id,
            "balance": balance
        }
        self.accounts.append(new_account)
        self.save_accounts()
        return new_account
        