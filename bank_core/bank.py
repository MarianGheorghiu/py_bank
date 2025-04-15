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
                       account_id, balance, account_type, creation_date,
                       friends, transactions):
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
            },
            "friends": friends,
            "transactions": transactions
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
        
        if "currency_accounts" not in user_account:
            user_account["currency_accounts"] = {}
            
        user_account["currency_accounts"][selected_currency] = {
        "account_id": currency_account_number,
        "balance": balance,
        "created_at": creation_date }
        
        self.save_accounts()
        print("Success. New currency added." )
        return True
    
    def switch_currency(self, selected_currency, user_account):
        selected_account = user_account["currency_accounts"][selected_currency]
        user_account["account_type"] = selected_currency
        user_account["balance"] = selected_account["balance"]
        user_account["creation_date"] = selected_account["created_at"]
        self.save_accounts()
        return True
    
    def exchange_currency(self, user_account, amount, current_currency, 
                          target_currency, converted_amount):
        user_account["balance"] -= amount
        user_account["currency_accounts"][current_currency]["balance"] -= amount
        user_account["currency_accounts"][target_currency]["balance"] += converted_amount
        self.save_accounts()
        return True
        
    
    # unele merg direct in bank_account sau vedem poate facem totul aici
    
    def add_friend(self, user_account, friend_id):
        default_friend = {
            "account_id": friend_id,
            "account_type": "EUR",
            "balance": float(0)
        }
        user_account["friends"].append(default_friend)
        self.save_accounts()
        return True
    
    def remove_friend(self, user_account, friend_id):
        for friend in user_account["friends"]:
            if isinstance(friend, dict) and friend.get("account_id") == friend_id:
                user_account["friends"].remove(friend)
                user_account["friends"].remove(friend_id)
                self.save_accounts()
                return True
        return False
    
    def find_friend_index(self, user_account, friend_id):
        for i, friend in enumerate(user_account["friends"]):
            if isinstance(friend, dict) and friend.get("account_id") == friend_id:
                return i
        return -1  # Return -1 if not found

    
    def send_money_to_friend(self, user_account, friend_id, amount, currency, date):
        friend_index = self.find_friend_index(user_account, friend_id) 
        if friend_index == -1: 
            print("Friend not found")
            return False
        # update all balances
        user_account["balance"] -= amount
        user_account["currency_accounts"][currency]["balance"] -= amount
        user_account["friends"][friend_index]["balance"] += amount
        
        # add in transactions history
        user_account["transactions"].append({
            "type": "friend_transfer",
            "amount": amount,
            "currency": currency,
            "friend_id": friend_id,
            "transfered_at": date
        })
        
        self.save_accounts()
        return True
        
    
    def close_account(self):
        pass
    
    def apply_loan(self):
        pass
        
# Afiseaza banii din toate conturile
# 