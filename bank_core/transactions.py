# Atribute (ID tranzacție, număr cont, tip (depunere/retragere/transfer), sumă, timestamp).
# Utilitară pentru urmărirea și gestionarea istoricului tranzacțiilor.
# Crearea unei clase separate Transaction poate ajuta la organizarea și 
# gestionarea istoricului tuturor tranzacțiilor efectuate pe diferite conturi
# transactions.py

class Transactions:
    def __init__(self, bank):
        self.bank = bank

    def add_money(self, account, amount, date):
        account["balance"] += amount
        currency = account['account_type']
        account['currency_accounts'][currency]['balance'] += amount

        transaction = {
            "type": "deposit",
            "account_id": account['account_id'],
            "amount": amount,
            "currency": account['account_type'],
            "date": date
        }
        account['transactions'].append(transaction)
        self.bank.save_accounts()
        print(f"✅ Added {amount} {account['account_type']} to your account.")

    def withdraw(self, account, amount, date):
        account["balance"] -= amount
        currency = account['account_type']
        account['currency_accounts'][currency]['balance'] -= amount
        
        transaction = {
            "type": "witdraw",
            "account_id": account['account_id'],
            "amount": amount,
            "currency": account['account_type'],
            "date": date
        }
        
        account['transactions'].append(transaction)
        self.bank.save_accounts()
        print(f"✅ Withdrawn {amount} {account['account_type']} from your account.")

    def transfer(self, from_account_id, to_account_id, amount):
        pass  # Logic will go here

    def get_balance(self, account_id):
        pass  # Logic will go here
    
    def record_friend_transfer(self, user_account, friend_id, amount, currency, date):
        transaction = {
            "type": "friend_transfer",
            "id": friend_id,
            "amount": amount,
            "currency": currency,
            "transfered_at": date
        }
        user_account["transactions"].append(transaction)
