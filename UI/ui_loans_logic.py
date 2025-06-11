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
        print(f"\n{'='*25}")
        print(f"  LOAN MANAGEMENT")
        print(f"{'='*25}")
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