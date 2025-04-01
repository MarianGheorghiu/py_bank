import uuid
from utils import hash_password, check_password

def start_cli(bank):
    logged_in = False
    current_user = None
    
    while True:
        if not logged_in:
            # Meniul pentru utilizatori neautentificați
            print("\n1. Create account")
            print("2. Login")
            print("3. Exit")
            
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
                balance = 0
                
                # Setam EURO by default
                account_type = 'EUR'
                
                # Encrypted password
                
                
                new_account = bank.create_account(first_name, last_name, hash_password(password),
                                                  account_number,account_id, balance,
                                                  account_type)
                print(f"Account created successfully!")
                print(f"Your Name: {first_name} {last_name}")
                print(f"Your account number: {account_number}")
                print(f"Password saved.")
                print(f"Your account ID: {account_id}")
                print(f"Initial balance: {balance}")
                print(f"Account type: {account_type}")
                
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
                
            elif choice == '3':
                break
                
        else:
            # Meniul pentru utilizatori autentificați
            print(f"\nLogged in as: {current_user['first_name']} {current_user['last_name']}")
            print("\n1. User Data")
            print("2. Logout")
            print("3. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                print("\nUser Data:")
                print(f"Name: {current_user['first_name']} {current_user['last_name']}")
                print(f"Account Number: {current_user['account_number']}")
                print(f"Account ID: {current_user['account_id']}")
                print(f"Balance: {current_user['balance']}")
                print(f"Account type: {current_user['account_type']}")
                
            elif choice == '2':
                logged_in = False
                current_user = None
                print("Logged out successfully")
                
            elif choice == '3':
                break