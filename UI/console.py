def start_cli(bank):
    while True:
        print("\n1. Create account")
        print("\n2. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            account_number = input("Account Number: ")
            account_id = input("Account ID: ")
            balance = float(input("Initial Balance: "))

            new_account = bank.create_account(first_name, last_name, account_number, account_id, balance)
            print(f"Account created: {new_account}")  # Afișează datele contului

        elif choice == '2':
            break
