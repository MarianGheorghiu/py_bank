import datetime
import sys

from utils import check_password, hash_password

def manage_settings(user_account, bank):
    while True:
        print(f"\n{'SETTINGS MENU:'}")
        print(f"{'─'*30}")
        print(" 1. Change First Name")
        print(" 2. Change Last Name")
        print(" 3. Change Password")
        print(" 4. Close Account")
        print(" 0. Return to Main Menu")
        print(f"{'─'*30}")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            change_first_name(user_account, bank)
        elif choice == "2":
            change_last_name(user_account, bank)
        elif choice == "3":
            change_password(user_account, bank)
        elif choice == "4":
            close_account(user_account, bank)
        else:
            print("Invalid option. Please try again.")

def change_first_name(user_account, bank):
    while True:
        print(f"\n{'='*25}")
        print(f"  CHANGE FIRST NAME")
        print(f"{'='*25}")
        print(f"Current First Name: {user_account['first_name']}")
        
        # Check if user can change name (monthly restriction)
        if not can_change_name(user_account, 'first_name'):
            last_change = user_account.get('name_changes', {}).get('first_name_last_changed')
            print(f"You can only change your first name once per month.")
            print(f"Last changed: {last_change}")
            print(f"Next change available: {get_next_change_date(last_change)}")
            print("\n0. Back to Settings")
            
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        print(f"\n{'OPTIONS:'}")
        print(f"{'─'*20}")
        print("1. Enter New First Name")
        print("0. Back to Settings")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            new_name = input("Enter new first name: ").strip()
            
            if not new_name:
                print("First name cannot be empty.")
                continue
            
            if len(new_name) < 2:
                print("First name must be at least 2 characters long.")
                continue
            
            if not new_name.replace(" ", "").replace("-", "").isalpha():
                print("First name can only contain letters, spaces, and hyphens.")
                continue
            
            # Confirm change
            print(f"\nCONFIRM CHANGE:")
            print(f"Current: {user_account['first_name']}")
            print(f"New: {new_name}")
            print("Remember: You can only change your name once per month!")
            
            confirm = input("Confirm change? (y/n): ").lower().strip()
            
            if confirm == 'y':
                # Update name and track change
                user_account['first_name'] = new_name
                track_name_change(user_account, 'first_name')
                bank.save_accounts()
                
                print(f"First name successfully changed to: {new_name}")
                input("Press Enter to continue...")
                break
            else:
                print("Change cancelled.")
        else:
            print("Invalid option. Please try again.")

def change_last_name(user_account, bank):
    while True:
        print(f"\n{'='*50}")
        print(f"  CHANGE LAST NAME")
        print(f"{'='*50}")
        print(f"Current Last Name: {user_account['last_name']}")
        
        # Check if user can change name (monthly restriction)
        if not can_change_name(user_account, 'last_name'):
            last_change = user_account.get('name_changes', {}).get('last_name_last_changed')
            print(f"You can only change your last name once per month.")
            print(f"Last changed: {last_change}")
            print(f"Next change available: {get_next_change_date(last_change)}")
            print("\n0. Back to Settings")
            
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        print(f"\n{'OPTIONS:'}")
        print(f"{'─'*20}")
        print("1. Enter New Last Name")
        print("0. Back to Settings")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            new_name = input("Enter new last name: ").strip()
            
            if not new_name:
                print("Last name cannot be empty.")
                continue
            
            if len(new_name) < 2:
                print("Last name must be at least 2 characters long.")
                continue
            
            if not new_name.replace(" ", "").replace("-", "").isalpha():
                print("Last name can only contain letters, spaces, and hyphens.")
                continue
            
            # Confirm change
            print(f"\nCONFIRM CHANGE:")
            print(f"Current: {user_account['last_name']}")
            print(f"New: {new_name}")
            print("Remember: You can only change your name once per month!")
            
            confirm = input("Confirm change? (y/n): ").lower().strip()
            
            if confirm == 'y':
                # Update name and track change
                user_account['last_name'] = new_name
                track_name_change(user_account, 'last_name')
                bank.save_accounts()
                
                print(f"Last name successfully changed to: {new_name}")
                input("Press Enter to continue...")
                break
            else:
                print("Change cancelled.")
        else:
            print("Invalid option. Please try again.")

def change_password(user_account, bank):
    while True:
        print(f"\n{'OPTIONS:'}")
        print(f"{'─'*20}")
        print("1. Change Password")
        print("0. Back to Settings")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            # Verify current password
            current_password = input("Enter current password: ").strip()
            is_same = check_password(user_account.get('password', ''), current_password)
            
            if not is_same:
                print("Current password is incorrect.")
                continue
            
            # Get new password
            new_password = input("Enter new password: ").strip()
            
            if len(new_password) < 4:
                print("Password must be at least 4 characters long.")
                continue
            
            # Confirm new password
            confirm_password = input("Confirm new password: ").strip()
            
            if new_password != confirm_password:
                print("Passwords do not match.")
                continue
            
            if new_password == current_password:
                print("New password must be different from current password.")
                continue
            
            # Update password
            user_account['password'] = hash_password(new_password)
            if not 'password_last_changed' in user_account:
                user_account['password_last_changed'] = ''
            user_account['password_last_changed'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bank.save_accounts()
            
            print("Password successfully changed!")
            input("Press Enter to continue...")
            break
        else:
            print("Invalid option. Please try again.")

def close_account(user_account, bank):
    while True:
        print(f"\n{'='*25}")
        print(f" CLOSE ACCOUNT")
        print(f"{'='*25}")
        print("WARNING: This action cannot be undone!")
        
        # Check for active loans
        active_loans = []
        if 'loans' in user_account:
            active_loans = [loan for loan in user_account['loans'] if loan.get('status') == 'active']
        
        if active_loans:
            print(f"\nCANNOT CLOSE ACCOUNT")
            print(f"You have {len(active_loans)} active loan(s):")
            for loan in active_loans:
                print(f"  • {loan['type']}: {loan['remaining_balance']:.2f} {loan['currency']}")
            print("\nPlease pay off all loans before closing your account.")
            print("\n0. Back to Settings")
            
            choice = input("Select an option: ").strip()
            if choice == "0":
                break
            continue
        
        # Show account summary
        print(f"\nACCOUNT SUMMARY:")
        print(f"{'─'*30}")
        print(f"Name: {user_account['first_name']} {user_account['last_name']}")
        print(f"Account ID: {user_account['account_id']}")
        print(f"Balance: {user_account['balance']:.2f} {user_account['account_type']}")
        
        # Show currency accounts
        if 'currency_accounts' in user_account:
            total_balance = 0
            print(f"\nCurrency Accounts:")
            for currency, acc in user_account['currency_accounts'].items():
                print(f"  {currency}: {acc['balance']:.2f}")
                total_balance += acc['balance']
            print(f"Total Balance: {total_balance:.2f} (equivalent)")
        
        print(f"\n{'OPTIONS:'}")
        print(f"{'─'*20}")
        print("1. Proceed with Account Closure")
        print("0. Back to Settings")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            # Final confirmation
            print(f"\n{'='*25}")
            print(f"FINAL CONFIRMATION")
            print(f"{'='*25}")
            print("LAST WARNING: This will permanently close your account!")
            print("All account data will be deleted and cannot be recovered.")
            print("Any remaining balance will be forfeited.")
            
            print(f"\nType 'DELETE MY ACCOUNT' to confirm:")
            confirmation = input().strip()
            
            if confirmation == "DELETE MY ACCOUNT":
                print(f"\nAccount {user_account['account_id']} has been closed.")
                print("Thank you for using our banking services.")
                
                print("\nAccount successfully closed.")
                print("\nIn 10 days you will be deleted from our database.")
                input("Press Enter to exit...")
                sys.exit(0)
            else:
                print("Account closure cancelled - confirmation text did not match.")
        else:
            print("Invalid option. Please try again.")

def can_change_name(user_account, name_type):
    if 'name_changes' not in user_account:
        return True
    
    last_change_key = f"{name_type}_last_changed"
    last_change = user_account['name_changes'].get(last_change_key)
    
    if not last_change:
        return True
    
    # Parse last change date
    try:
        last_change_date = datetime.datetime.strptime(last_change, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        
        # Check if a month has passed
        if now.month != last_change_date.month or now.year != last_change_date.year:
            return True
        else:
            return False
    except:
        return True

def track_name_change(user_account, name_type):

    if 'name_changes' not in user_account:
        user_account['name_changes'] = {}
    
    user_account['name_changes'][f"{name_type}_last_changed"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_next_change_date(last_change_str):
    try:
        last_change = datetime.datetime.strptime(last_change_str, "%Y-%m-%d %H:%M:%S")
        # Add one month
        if last_change.month == 12:
            next_change = last_change.replace(year=last_change.year + 1, month=1)
        else:
            next_change = last_change.replace(month=last_change.month + 1)
        return next_change.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Unknown"