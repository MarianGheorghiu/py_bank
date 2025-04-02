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
    
    def create_account(self, first_name, last_name, password, account_number, 
                       account_id, balance, account_type, creation_date):
        new_account = {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "account_number": account_number,
            "account_id": account_id,
            "balance": balance,
            "account_type": account_type,
            "creation_date": creation_date,
            "currency_accounts": {
                "EUR": {
                    "account_id": account_id,
                    "balance": balance,
                    "created_at": creation_date
                }
            }
        }
        self.accounts.append(new_account)
        self.save_accounts()
        return new_account
    
    def get_account_by_id(self, id):
        for account in self.accounts:
            if account['account_id'] == id:
                return account
        return False
    
    def add_new_currency_account(self, user_id, selected_currency, 
                                 currency_account_number, 
                                 balance, creation_date):
        
        user_account = self.get_account_by_id(user_id)

        if not user_account:
            return "Account does not exist."
        if selected_currency in user_account["currency_accounts"]:
            print("You already have this currency!")
            return False
        
        # Add the new currency to account_types
        user_account["account_type"].append(selected_currency)
        
        if "currency_accounts" not in user_account:
            user_account["currency_accounts"] = {}
            
        user_account["currency_accounts"][selected_currency] = {
        "account_id": currency_account_number,
        "balance": balance,
        "created_at": creation_date }
        
        self.save_accounts()
        print("Success. New currency added." )
        return True
        
    
    # unele merg direct in bank_account sau vedem poate facem totul aici
    def find_account(self):
        pass
    
    def close_account(self):
        pass
    
    def add_friend(self):
        pass
    
    def remove_friend(self):
        pass
    
    def apply_loan(self):
        pass
        