import uuid
import datetime
import json
from utils import hash_password, check_password

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
            print("\nManage Account:")
            print("1. Account info")
            print("2. Add new currency")
            print("3. Switch currency")
            print("4. Show currencies")
            print("0. Go back")
            
            account_choice = input("Select an option: ")
            
            if account_choice == '1':
                print("\n---Account Details---")
                print(f"Name: {current_user['first_name']} {current_user['last_name']}")
                print(f"Account Number: {current_user['account_number']}")
                print(f"Account ID: {current_user['account_id']}")
                print(f"Currency: {current_user['account_type']}")
                print(f"Balance: {current_user['balance']}")
                print(f"Registered at: {current_user['creation_date']}")
                
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
             
def switch_currency_account(current_user, bank):
    while True:
        current_currency = current_user["account_type"]
        print(f"\nYour currency is in {current_currency}. Switch to:")
                
        # Create a list of available currencies excluding the current one
        available_currencies = ["USD", "GBP", "YEN", "EUR"]
        
        # Filter out currencies the user doesn't have
        if "currency_accounts" in current_user:
            available_currencies = [curr for curr in current_user["currency_accounts"] 
                                    if curr != current_currency]
        
        # Display available currencies as menu options
        if not available_currencies:
            print("You don't have any other currency accounts to switch to.")
            return
        
        # Display numbered menu options for each available currency
        for i, currency in enumerate(available_currencies, 1):
            print(f"{i}. {currency}")
            
        print("0. Go back")
        
        # Get user choice
        choice = input("Select an option: ")
        
        if choice == '0':
            break  # Return to the previous menu
        
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(available_currencies):
                selected_currency = available_currencies[choice_index]
                # Add code here to actually switch the currency
                bank.switch_currency(selected_currency, current_user)
                print(f"Successfully switched to {selected_currency}!")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a number.")
                
def add_new_currency(current_user, bank):
    print("\nSelect currency for new account:")
    print("1. USD")
    print("2. GBP")
    print("3. YEN")
    print("0. Go back")
        
    currency_choice = input("Select currency: ")
    
    if currency_choice == '0':
        return
        
    if currency_choice in ['1', '2', '3']:
        currency_map = {'1': 'USD', '2': 'GBP', '3': 'YEN'}
        # generate currency account data
        selected_currency = currency_map[currency_choice]
        currency_account_number = str(uuid.uuid4().int)[:4]
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #  add full data to new currency account
        result = bank.add_new_currency_account(current_user['account_id'], 
                                        selected_currency,
                                        currency_account_number,
                                        float(0),
                                        creation_date)
            
        if result:
            # Here you would add code to create a new account
            print(f"New {selected_currency} currency added!")
        else:
            print("Invalid currency choice.")
            
def display_user_currency_accounts(current_user):
    print(" ")
    print("Your currency accounts:")
    for i, currency in enumerate(current_user["currency_accounts"], 1):
        print(f"{i}. {currency}")
        
def exchange_currencies(current_user, bank):
    # Display current account info
    current_currency = current_user['account_type']
    current_balance = current_user['balance']
    
    print(f"\nYour current account is in {current_currency} and you have {current_balance:.2f} balance.")
    
    # Get available currencies except the current one
    available_currencies = [currency for currency in current_user['currency_accounts'].keys() 
                           if currency != current_currency]
    
    if not available_currencies:
        print("You don't have any other currency accounts to exchange with.")
        return
    
    # Display available currencies
    print("Available currencies to exchange to:")
    for i, currency in enumerate(available_currencies, 1):
        print(f"{i}. {currency}")
    print("0. Go back")
    
    # Get target currency choice from user
    while True:
        try:
            choice = input("\nSelect the currency you want to exchange to (0 to exit): ")
            
            if choice == '0':
                return
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_currencies):
                target_currency = available_currencies[choice_idx]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Get amount to exchange
    while True:
        try:
            if current_balance <= 0:
                print("You don't have money.")
                break
            amount_str = input(f"\nHow much {current_currency} do you want to exchange to {target_currency}: ")
            amount = float(amount_str)
            
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
                
            if amount > current_user['balance']:
                print(f"Insufficient funds. Your {current_currency} balance is {current_balance:.2f}.")
                continue
                
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Apply exchange rate (this is a simplified example)
    # In a real application, you would use an API or database for current exchange rates
    exchange_rates = {
        'EUR_USD': 1.08,
        'USD_EUR': 0.93,
        'EUR_GBP': 0.85,
        'GBP_EUR': 1.18,
        'EUR_YEN': 163.50,
        'YEN_EUR': 0.0061,
        'USD_GBP': 0.79,
        'GBP_USD': 1.27,
        'USD_YEN': 151.40,
        'YEN_USD': 0.0066,
        'GBP_YEN': 192.35,
        'YEN_GBP': 0.0052
    }
        
    rate_key = f"{current_currency}_{target_currency}"
    if rate_key in exchange_rates:
        rate = exchange_rates[rate_key]
    else:
        # Fallback or reverse lookup
        reverse_key = f"{target_currency}_{current_currency}"
        if reverse_key in exchange_rates:
            rate = 1 / exchange_rates[reverse_key]
        else:
            print(f"Exchange rate for {current_currency} to {target_currency} not available.")
            return
    
    converted_amount = amount * rate
    
    # Confirm exchange
    print(f"\n{amount:.2f} {current_currency} is {converted_amount:.2f} {target_currency}.")
    print("Do you want to exchange?")
    print("1. Yes")
    print("2. No")
    print("0. Abort")
    
    confirm = input("Your choice: ")
    
    if confirm == '1':
        # Process exchange
        bank.exchange_currency(current_user, amount, current_currency, 
                               target_currency, converted_amount)
        
        print(f"\nExchange successful!")
        print(f"New {current_currency} balance: {current_user['balance']:.2f}")
        print(f"New {target_currency} balance: {current_user['currency_accounts'][target_currency]['balance']:.2f}")
    elif confirm == '2':
        print("Exchange cancelled.")
    else:
        print("Returning to previous menu.")
        
def manage_friends(current_user, bank):
    while True:
        print("\nFriend Manager Menu")
        print("1. Add Friend")
        print("2. Find Friend")
        print("3. Remove Friend")
        print("4. Show All Friends")
        print("5. Send Money to a Friend") 
        print("0. Go back")

        choice = input("Choose an option: ")

        if choice == "1":
            friend = input("Enter your friend id: ").strip()
            if friend in current_user['friends']:
                print(f"{friend} is already your friend.")
            else:
                current_user['friends'].append(friend)
                bank.add_friend(current_user, friend)
                print(f"Friend added successfully.")

        elif choice == "2":
            search_id = input("Enter friend id: ").strip()
            if search_id in current_user['friends']:
                print(f"{search_id} is in your friends list.")
            else:
                print(f"{search_id} not found.")

        elif choice == "3":
            to_remove = input("Enter friend id to remove: ").strip()
            if to_remove in current_user['friends']:
                bank.remove_friend(current_user, to_remove);
                print(f"{to_remove} has been removed.")
            else:
                print(f"{to_remove} not found in your friends list.")

        elif choice == "4":
            friends = current_user['friends']
            if not friends or all(not isinstance(fr, dict) for fr in friends):
                print("Your friends list is empty.")
            else:
                print("\nYour Friends:\n")
                print(f"{'No.':<5} {'Account ID':<15} {'Currency':<10} {'Balance':>10}")
                print("-" * 45)
                count = 1
                for fr in friends:
                    if isinstance(fr, dict):
                        print(f"{count:<5} {fr['account_id']:<15} {fr['account_type']:<10} {fr['balance']:>10.2f}")
                        count += 1

        elif choice == "5":
                # Display friends list for selection
                friends = current_user['friends']
                if not friends:
                    print("Your friends list is empty.")
                    continue
                
                print("\nYour Friends:")
                valid_friends = []
                count = 1
                for fr in friends:
                    if isinstance(fr, dict):
                        print(f"{count}. ID: {fr['account_id']} - Currency: {fr['account_type']}")
                        valid_friends.append(fr)
                        count += 1
                
                if not valid_friends:
                    print("No valid friends found.")
                    continue
                
                # Select friend
                try:
                    selection = int(input("\nSelect friend by number: "))
                    if 1 <= selection <= len(valid_friends):
                        selected_friend = valid_friends[selection-1]
                        friend_id = selected_friend['account_id']
                        friend_currency = selected_friend['account_type']
                    else:
                        print("Invalid selection.")
                        continue
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                
                # Select currency (if user has multiple)
                available_currencies = list(current_user.get('currency_accounts', {}).keys())
                if not available_currencies:
                    print("You don't have any currency accounts.")
                    continue
                
                if len(available_currencies) > 1:
                    print("\nSelect currency to send:")
                    for i, curr in enumerate(available_currencies, 1):
                        balance = current_user['currency_accounts'][curr]['balance']
                        print(f"{i}. {curr} - Balance: {balance}")
                    
                    try:
                        curr_selection = int(input("Choose currency (number): "))
                        if 1 <= curr_selection <= len(available_currencies):
                            currency = available_currencies[curr_selection-1]
                        else:
                            print("Invalid selection.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                else:
                    currency = available_currencies[0]
                
                # Check currency compatibility
                if currency != friend_currency:
                    print(f"Currency mismatch. Your friend accepts {friend_currency} but you selected {currency}.")
                    continue
                
                # Enter amount
                try:
                    amount = float(input("\nEnter amount to send: "))
                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue
                        
                    # Check if user has enough balance
                    user_balance = current_user['currency_accounts'][currency]['balance']
                    if amount > user_balance:
                        print(f"Insufficient funds. Your {currency} balance is {user_balance}.")
                        continue
                        
                except ValueError:
                    print("Please enter a valid amount.")
                    continue
                
                # Call bank method to process the transfer
                transefered_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = bank.send_money_to_friend(current_user, friend_id, amount,
                                                   currency, transefered_at)
                
                if result:
                    print(f"\nSuccessfully sent {amount} {currency} to friend (ID: {friend_id}).")
                else:
                    print("Transaction failed. Please try again.")

        elif choice == "0":
            print("Exiting Friend Manager.")
            break

        else:
            print("Invalid choice. Please try again.")

def manage_transactions(user_account, transactions):
    while True:
        print("\n--- Transactions Menu ---")
        print("1. Add Money")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Show Transactions")
        print("5. Find Transaction")
        print("0. Go Back")

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
                print("❌ Insufficient funds.")
                break
            transactions.withdraw(user_account, amount, date)
            
        elif choice == "3":
            to_id = input("Enter recipient account ID: ")
            
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
                print("\n📄 Transaction History:\n")
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

def manage_settings(user_account, bank):
    # change first name, last name - remember 1 change for 1 month, close account
    # if user has loan, dont allow to close account
    # change password, add phone number
    pass
    
def manage_loans(current_account, bank):
    # Initialize loans if not present
    if "loans" not in current_account:
        current_account["loans"] = []
    
    # Define available loan types with their characteristics
    loan_types = {
        "1": {
            "name": "Home Loan",
            "description": "Mortgage for purchasing or refinancing a home",
            "max_multiplier": 15,  # Can loan up to 15x balance
            "interest_rate": 3.5,
            "term_years": 30
        },
        "2": {
            "name": "Car Loan", 
            "description": "Auto financing for vehicle purchase",
            "max_multiplier": 8,   # Can loan up to 8x balance
            "interest_rate": 5.2,
            "term_years": 7
        },
        "3": {
            "name": "Personal Loan",
            "description": "Unsecured loan for personal expenses",
            "max_multiplier": 5,   # Can loan up to 5x balance
            "interest_rate": 8.9,
            "term_years": 5
        },
        "4": {
            "name": "Business Loan",
            "description": "Funding for business operations or expansion", 
            "max_multiplier": 12,  # Can loan up to 12x balance
            "interest_rate": 6.8,
            "term_years": 10
        }
    }
    
    # Get user's primary account balance
    primary_balance = current_account["balance"]
    currency = current_account["account_type"]
    
    while True:
        # Display main loan menu
        print(f"\n{'='*50}")
        print(f"  LOAN MANAGEMENT")
        print(f"{'='*50}")
        print(f"Welcome {current_account['first_name']} {current_account['last_name']}")
        print(f"Balance: {primary_balance:.2f} {currency}")
        
        # Show loan summary
        active_loans = len([loan for loan in current_account["loans"] if loan.get("status") == "active"])
        if active_loans > 0:
            print(f"Active Loans: {active_loans}")
        
        print(f"\n{'MAIN MENU:'}")
        print(f"{'─'*30}")
        print("1. Apply for New Loan")
        print("2. View My Loans")
        print("3. Make Loan Payment")
        print("0. Return to Main Menu")
        print(f"{'─'*30}")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            show_loan_application_menu(current_account, bank, loan_types, currency)
        elif choice == "2":
            view_loan_details(current_account)
        elif choice == "3":
            make_loan_payment(current_account, bank)
        else:
            print("Invalid option. Please try again.")

def show_loan_application_menu(current_account, bank, loan_types, currency):

    primary_balance = current_account["balance"]
    
    while True:
        print(f"\n{'='*50}")
        print(f"  LOAN APPLICATION")
        print(f"{'='*50}")
        print(f"Your Balance: {primary_balance:.2f} {currency}")
        
        print(f"\n{'Available Loan Types:'}")
        print(f"{'─'*40}")
        
        # Display loan options cleanly
        for key, loan in loan_types.items():
            max_loan = primary_balance * loan["max_multiplier"]
            print(f"{key}. {loan['name']}")
            print(f"   Max: {max_loan:.2f} {currency} | Rate: {loan['interest_rate']}% | {loan['term_years']} years")
            print()
        
        print("0. Back to Loan Menu")
        print(f"{'─'*40}")
        
        choice = input("Select loan type: ").strip()
        
        if choice == "0":
            break
        elif choice in loan_types:
            apply_for_loan(current_account, bank, loan_types[choice], currency)
            break  # Return to main menu after application
        else:
            print("Invalid option. Please try again.")

def apply_for_loan(current_account, bank, loan_info, currency):
    """
    Handle loan application process
    """
    max_loan = current_account["balance"] * loan_info["max_multiplier"]
    
    print(f"\n{'─'*50}")
    print(f"  APPLYING FOR {loan_info['name'].upper()}")
    print(f"{'─'*50}")
    print(f"Maximum eligible amount: {max_loan:.2f} {currency}")
    print(f"Interest Rate: {loan_info['interest_rate']}%")
    print(f"Loan Term: {loan_info['term_years']} years")
    
    try:
        requested_amount = float(input(f"\nEnter loan amount (max {max_loan:.2f}): "))
        
        if requested_amount <= 0:
            print("Loan amount must be positive.")
            return
            
        if requested_amount > max_loan:
            print(f"Requested amount exceeds maximum eligible amount of {max_loan:.2f} {currency}")
            return
        
        # Calculate monthly payment
        monthly_rate = loan_info["interest_rate"] / 100 / 12
        num_payments = loan_info["term_years"] * 12
        
        if monthly_rate > 0:
            monthly_payment = requested_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = requested_amount / num_payments
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - requested_amount
        
        # Show loan summary
        print(f"\n{'LOAN SUMMARY:'}")
        print(f"{'─'*30}")
        print(f"Loan Amount: {requested_amount:.2f} {currency}")
        print(f"Monthly Payment: {monthly_payment:.2f} {currency}")
        print(f"Total Interest: {total_interest:.2f} {currency}")
        print(f"Total Payment: {total_payment:.2f} {currency}")
        
        confirm = input("\nConfirm loan application? (y/n): ").lower().strip()
        
        if confirm == 'y':
            # Create loan record
            import datetime
            loan_record = {
                "loan_id": f"LOAN{len(current_account['loans']) + 1:04d}",
                "type": loan_info["name"],
                "amount": requested_amount,
                "currency": currency,
                "interest_rate": loan_info["interest_rate"],
                "term_years": loan_info["term_years"],
                "monthly_payment": monthly_payment,
                "remaining_balance": requested_amount,
                "total_payments": 0,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "active"
            }
            
            # Save changes
            bank.apply_loan(current_account, loan_record, requested_amount)
            
            print(f"Loan approved! {requested_amount:.2f} {currency} has been added to your account.")
            print(f"Loan ID: {loan_record['loan_id']}")
        else:
            print("Loan application cancelled.")
            
    except ValueError:
        print("Invalid amount entered.")

def view_loan_details(current_account):
    """
    Display detailed information about user's loans in a separate menu
    """
    while True:
        print(f"\n{'='*50}")
        print(f"  MY LOANS")
        print(f"{'='*50}")
        
        if not current_account.get("loans"):
            print("You have no loans.")
            print("\n0. Back to Loan Menu")
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        # Display loans
        active_loans = []
        paid_loans = []
        
        for loan in current_account["loans"]:
            if loan.get("status") == "active":
                active_loans.append(loan)
            else:
                paid_loans.append(loan)
        
        if active_loans:
            print("ACTIVE LOANS:")
            print("─" * 40)
            for i, loan in enumerate(active_loans, 1):
                print(f"{i}. {loan['type']} (ID: {loan['loan_id']})")
                print(f"   Balance: {loan['remaining_balance']:.2f} {loan['currency']}")
                print(f"   Monthly Payment: {loan['monthly_payment']:.2f} {loan['currency']}")
                print(f"   Rate: {loan['interest_rate']}%")
                print()
        
        if paid_loans:
            print("PAID OFF LOANS:")
            print("─" * 40)
            for loan in paid_loans:
                print(f"• {loan['type']} - {loan['amount']:.2f} {loan['currency']} (PAID OFF)")
            print()
        
        print("OPTIONS:")
        print("─" * 20)
        if active_loans:
            print("1. View Detailed Loan Info")
        print("0. Back to Loan Menu")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1" and active_loans:
            show_detailed_loan_info(active_loans)
        else:
            print("Invalid option. Please try again.")

def show_detailed_loan_info(active_loans):
    print(f"\n{'='*50}")
    print(f"  DETAILED LOAN INFORMATION")
    print(f"{'='*50}")
    
    for i, loan in enumerate(active_loans, 1):
        print(f"{i}. {loan['type']}")
    
    print("0. Back")
    
    try:
        choice = int(input("Select loan to view details: ")) - 1
        
        if choice == -1:  # User selected 0
            return
        elif 0 <= choice < len(active_loans):
            loan = active_loans[choice]
            
            print(f"\n{'='*50}")
            print(f"  {loan['type'].upper()} DETAILS")
            print(f"{'='*50}")
            print(f"Loan ID: {loan['loan_id']}")
            print(f"Original Amount: {loan['amount']:.2f} {loan['currency']}")
            print(f"Remaining Balance: {loan['remaining_balance']:.2f} {loan['currency']}")
            print(f"Monthly Payment: {loan['monthly_payment']:.2f} {loan['currency']}")
            print(f"Interest Rate: {loan['interest_rate']}%")
            print(f"Loan Term: {loan['term_years']} years")
            print(f"Total Payments Made: {loan['total_payments']}")
            print(f"Created: {loan['created_date']}")
            print(f"Status: {loan['status'].title()}")
            
            input("\nPress Enter to continue...")
        else:
            print("Invalid selection.")
            
    except ValueError:
        print("Invalid input.")

def make_loan_payment(current_account, bank):
    while True:
        print(f"\n{'='*50}")
        print(f"  MAKE LOAN PAYMENT")
        print(f"{'='*50}")
        print(f"Your Balance: {current_account['balance']:.2f} {current_account['account_type']}")
        
        if not current_account.get("loans"):
            print("❌ You have no loans to pay.")
            print("\n0. Back to Loan Menu")
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        active_loans = [loan for loan in current_account["loans"] if loan.get("status") == "active"]
        
        if not active_loans:
            print("You have no active loans to pay.")
            print("\n0. Back to Loan Menu")
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        print("\nSELECT LOAN TO PAY:")
        print("─" * 30)
        
        for i, loan in enumerate(active_loans, 1):
            print(f"{i}. {loan['type']}")
            print(f"   Balance: {loan['remaining_balance']:.2f} {loan['currency']}")
            print(f"   Monthly Payment: {loan['monthly_payment']:.2f} {loan['currency']}")
            print()
        
        print("0. Back to Loan Menu")
        
        try:
            choice = input("Select loan to pay: ").strip()
            
            if choice == "0":
                break
            
            loan_choice = int(choice) - 1
            
            if loan_choice < 0 or loan_choice >= len(active_loans):
                print("Invalid loan selection.")
                continue
            
            # Process the payment
            process_loan_payment(active_loans[loan_choice], current_account, bank)
            
        except ValueError:
            print("Invalid input.")

def process_loan_payment(selected_loan, current_account, bank):
    """
    Process individual loan payment
    """
    print(f"\n{'='*50}")
    print(f"  PAYMENT FOR {selected_loan['type'].upper()}")
    print(f"{'='*50}")
    
    max_payment = min(current_account["balance"], selected_loan["remaining_balance"])
    
    print(f"Loan Balance: {selected_loan['remaining_balance']:.2f} {selected_loan['currency']}")
    print(f"Monthly Payment: {selected_loan['monthly_payment']:.2f} {selected_loan['currency']}")
    print(f"Your Balance: {current_account['balance']:.2f} {current_account['account_type']}")
    print(f"Maximum Payment: {max_payment:.2f} {selected_loan['currency']}")
    
    try:
        payment_amount = float(input(f"\nEnter payment amount: "))
        
        if payment_amount <= 0:
            print("Payment amount must be positive.")
            input("Press Enter to continue...")
            return
        
        if payment_amount > max_payment:
            print(f"Payment amount exceeds maximum of {max_payment:.2f}")
            input("Press Enter to continue...")
            return
        
        # Confirm payment
        print(f"\nCONFIRM PAYMENT:")
        print(f"Amount: {payment_amount:.2f} {selected_loan['currency']}")
        print(f"For: {selected_loan['type']}")
        
        confirm = input("Confirm payment? (y/n): ").lower().strip()
        
        if confirm == 'y':
            # Save changes
            bank.pay_loan(current_account, selected_loan, payment_amount)
        else:
            print("Payment cancelled.")
        
        input("Press Enter to continue...")
        
    except ValueError:
        print("Invalid amount entered.")
        input("Press Enter to continue...")