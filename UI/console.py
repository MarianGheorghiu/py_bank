import uuid
import datetime
import json

from utils import hash_password, check_password
from .ui_loans_logic import manage_loans
from .ui_friends_logic import manage_friends
from .ui_currency_logic import switch_currency_account, add_new_currency, display_user_currency_accounts, exchange_currencies
from .ui_settings_logic import manage_settings

# Setam EURO by default
account_type = 'EUR'
friends = []
acc_transactions = []

def start_cli(bank, transactions):
    logged_in = False
    current_user = None
    
    while True:
        if not logged_in:
            # Meniul pentru utilizatori neautentificați
            print("\n1. Create account")
            print("2. Login")
            print("0. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                # add e-mail
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                password = input("Password (min. 4 chars): ")
                password_check = input("Repeat password: ")
                
                if password != password_check or len(password) < 4:
                    print("You did something wrong. Create account again.")
                    break
                    
                # Generare automată account_number folosind uuid
                account_number = str(uuid.uuid4())
                
                # Generare automată account_id - primele 4 cifre din alt uuid
                account_id = str(uuid.uuid4().int)[:4]
                
                # Setează balance la 0 pentru cont nou
                balance = float(0)
                
                # Creation date
                creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                
                new_account = bank.create_account(first_name, last_name, hash_password(password),
                                                  account_number,account_id, balance,
                                                  account_type, creation_date, 
                                                  friends, acc_transactions)
                print(f"Account created successfully!")
                print(f"Your Name: {first_name} {last_name}")
                print(f"Your account number: {account_number}")
                print(f"Password saved.")
                print(f"Your account ID: {account_id}")
                print(f"Initial balance: {balance}")
                print(f"Account type: {account_type}")
                print(f"Creation date: {creation_date}")
                
                # Autentificare automată după creare cont
                logged_in = True
                current_user = new_account
                
            elif choice == '2':
                account_id = input("Account ID: ")
                input_password = input("Password: ")
                # Aici ar trebui să adaugi și parola pentru autentificare
                # password = input("Password: ")
                
                # Verifică dacă există contul în baza de date
                user = bank.get_account_by_id(account_id)
                correct_password = check_password(user["password"], input_password)
                if user and correct_password:
                    logged_in = True
                    current_user = user
                else:
                    print("Invalid account ID")
                
            elif choice == '0':
                break
                
        else:
             # Meniul pentru utilizatori autentificați
            print(f"\nLogged in as: {current_user['first_name']} {current_user['last_name']}")
            print("\n1. Manage Account")
            print("2. Exchange Currencies")
            print("3. Transactions")
            print("4. Friends")
            print ("5. Loans")
            print("6. Settings")
            print("7. Logout")
            print("0. Exit")
            
            choice = input("Select an option: ")
                
            if choice == '1':
                manage_account(current_user, bank)
                
            elif choice == '2':
                exchange_currencies(current_user, bank)
                
            elif choice == '3':
                manage_transactions(current_user, transactions)
            
            elif choice == '4':
                manage_friends(current_user, bank)
                
            elif choice == '5':
                manage_loans(current_user, bank)
                
            elif choice == '6':
                manage_settings(current_user, bank)
                
            elif choice == '7':
                logged_in = False
                current_user = None
                print("Logged out successfully")
                
            elif choice == '0':
                break
            
            
def manage_account(current_user, bank):
    while True:
            print(f"\n{'='*20}")
            print(" Manage Account:")
            print(f"{'='*20}")
            print(" 1. Account info")
            print(" 2. Add new currency")
            print(" 3. Switch currency")
            print(" 4. Show currencies")
            print(" 0. Go back")
            
            account_choice = input("Select an option: ")
            
            if account_choice == '1':
                print(f"{'='*20}")
                print(" Account Details")
                print(f"{'='*20}")
                print(f" Name: {current_user['first_name']} {current_user['last_name']}")
                print(f" Account Number: {current_user['account_number']}")
                print(f" Account ID: {current_user['account_id']}")
                print(f" Currency: {current_user['account_type']}")
                print(f" Balance: {current_user['balance']}")
                print(f" Registered at: {current_user['creation_date']}")
                
            elif account_choice == '2':
                add_new_currency(current_user, bank)    
            elif account_choice == '3':
                switch_currency_account(current_user, bank)
            elif account_choice == '4':
                display_user_currency_accounts(current_user)
            elif account_choice == '0':
                break  # Return to the main menu 
            else:
                print("Invalid choice. Please try again.")
             
def manage_transactions(user_account, transactions):
    while True:
        print(f"{'='*20}")
        print(" Transactions Menu")
        print(f"{'='*20}")
        print(" 1. Add Money")
        print(" 2. Withdraw")
        print(" 3. Transfer")
        print(" 4. Show Transactions")
        print(" 5. Find Transaction")
        print(" 0. Go Back")

        choice = input("Choose an option: ")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if choice == "1":
            amount = float(input("Enter amount to add (max 2k): "))
            if amount >= 2000:
                print('You added too much. Bye!')
                continue
            transactions.add_money(user_account, amount, date)
            
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            if amount > user_account["balance"]:
                print("Insufficient funds.")
                break
            transactions.withdraw(user_account, amount, date)
            
        elif choice == "3":
            print("WARNING! FRIENDS NOT INCUDED !!!")
            to_id = input("Enter account ID: ")
            
            with open('bank_data/accounts.json', 'r') as file:
                users_data = json.load(file)
    
            # Check if recipient exists
            recipient = None
            for user in users_data:
                if user["account_id"] == to_id:
                    recipient = user
                    break
            
            if not recipient:
                print(f"Error: Recipient with account ID {to_id} not found.")
                return
            
            # Display available currencies for the recipient
            print(f"\nRecipient {recipient['first_name']} {recipient['last_name']} can accept:")
            available_currencies = list(recipient["currency_accounts"].keys())
            for i, currency in enumerate(available_currencies, 1):
                print(f"{i}. {currency}")
            
            # Let user select currency
            currency_choice = int(input("\nSelect currency to transfer (number): ")) - 1
            if currency_choice < 0 or currency_choice >= len(available_currencies):
                print("Invalid selection.")
                return
            
            selected_currency = available_currencies[currency_choice]
            
            # Check if sender has this currency account
            if selected_currency not in user_account["currency_accounts"]:
                print(f"You don't have a {selected_currency} account to transfer from.")
                return
            
            # Get transfer amount
            amount = float(input(f"Enter amount to transfer in {selected_currency}: "))
            
            # Check sufficient funds
            sender_balance = user_account["currency_accounts"][selected_currency]["balance"]
            has_enough = sender_balance - amount
            if has_enough < amount:
                print(f"Insufficient funds. {has_enough} after transfer.")
                return
            
            # Confirm transfer
            print(f"\nTransfer summary:")
            print(f"Sending {amount} {selected_currency} to {recipient['account_id']}")
            print(f"Your balance after transfer will be {has_enough} {selected_currency}")
            confirm = input("Confirm transfer (y/n): ").lower()
            
            if confirm != 'y':
                print("Transfer cancelled.")
                return
            
            transactions.transfer(user_account['account_id'], to_id, amount, 
                                  selected_currency, date)
            
                
        elif choice == "4":
            transactions = user_account.get("transactions", [])

            if not transactions:
                print("No transactions found.")
            else:
                # Header
                print("\nTransaction History:\n")
                print(f"{'No.':<5} {'ID':<5} {'Type':<15} {'Amount':<10} {'Currency':<10} {'Date':<10}")
                print("-" * 70)  # Separator line

                # Loop through transactions and print each row
                for i, tx in enumerate(transactions, start=1):
                    tx_type = tx.get("type", "-")
                    amount = tx.get("amount", "-")
                    currency = tx.get("currency", "-")
                    date = tx.get("date", tx.get("timestamp", "-"))
                    account_id = tx.get("account_id", "-")
                    index = f"{i}."
                    print(f"{index:<5} {account_id:<5} {tx_type:<15} {amount:<10} {currency:<10} {date:<10}")

                print("-" * 70)  # End separator line

        elif choice == "5":
            keyword = input("Enter id/type/etc. to search: ")
            matches = [tx for tx in user_account.get("transactions", []) if keyword in str(tx)]
            for m in matches:
                print(m)
                
        elif choice == "0":
            break
        
        else:
            print("Invalid choice. Please try again.")

