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
        account['currency_accounts'][currency]['balance'] = account["balance"]

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
        account['currency_accounts'][currency]['balance'] = account["balance"]
        
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

    def transfer(self, account_id, to_account_id, amount, 
                 selected_currency, date):
        account = None
        to_account = None
        # update users to correct saving
        for acc in self.bank.accounts:
            if acc["account_id"] == account_id:
                account = acc
            if acc["account_id"] == to_account_id:
                to_account = acc
        # update user balance
        account["balance"] -= amount
        account["currency_accounts"][selected_currency]["balance"] = account["balance"]
        # update transfered money
        to_account["balance"] += amount
        to_account["currency_accounts"][selected_currency]["balance"] = to_account["balance"]
        
        # update sender transaction
        sender_transaction = {
            "type": "transfer_out",
            "account_id": account_id,
            "transfer_to": to_account_id,
            "amount": amount,
            "currency": selected_currency,
            "date": date
        }
        
        receiver_transaction = {
            "type": "transfer_in",
            "account_id": to_account_id,
            "received_from": account_id,
            "amount": amount,
            "currency": selected_currency,
            "date": date
        }
        # save transactions
        account["transactions"].append(sender_transaction)
        to_account["transactions"].append(receiver_transaction)
        
        # update database
        self.bank.save_accounts()
        print(f"✅ Transfered from {account["account_id"]} to {to_account["account_id"]}.")

    def get_balance(self, account_id):
        pass  # Logic will go here
    
    def record_friend_transfer(self, user_account, friend_id, amount, currency, date):
        transaction = {
            "type": "friend_transfer",
            "account_id": friend_id,
            "amount": amount,
            "currency": currency,
            "date": date
        }
        user_account["transactions"].append(transaction)
