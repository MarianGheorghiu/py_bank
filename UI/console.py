import uuid
import datetime
from utils import hash_password, check_password

# Setam EURO by default
account_type = 'EUR'

def start_cli(bank):
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
                                                  account_type, creation_date)
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
            print("\n1. User Data")
            print("2. Manage Account")
            print("3. Exchange Currencies")
            print("4. Logout")
            print("0. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                print("\nUser Data:")
                print(f"Name: {current_user['first_name']} {current_user['last_name']}")
                print(f"Account Number: {current_user['account_number']}")
                print(f"Account ID: {current_user['account_id']}")
                print(f"Balance: {current_user['balance']}")
                print(f"Account type: {current_user['account_type']}")
                
            elif choice == '2':
                manage_account(current_user, bank)
                
            elif choice == '3':
                exchange_currencies(current_user, bank)
                
            elif choice == '4':
                logged_in = False
                current_user = None
                print("Logged out successfully")
                
            elif choice == '0':
                break
            
            
def manage_account(current_user, bank):
    while True:
            print("\nManage Account:")
            print("1. Show your current account")
            print("2. Add new currency")
            print("3. Switch currency")
            print("4. Show currencies")
            print("0. Go back")
            
            account_choice = input("Select an option: ")
            
            if account_choice == '1':
                print("\nCurrent Account Details:")
                print(f"Account Number: {current_user['account_number']}")
                print(f"Account ID: {current_user['account_id']}")
                print(f"Balance: {current_user['balance']}")
                print(f"Account types: {current_user['account_type']}")
                
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
    print("0. Exit")
    
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
    print("0. Exit")
    
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