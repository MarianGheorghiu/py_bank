import datetime

def manage_friends(current_user, bank):
    while True:
        print(f"{'='*20}")
        print("Friend Manager Menu")
        print(f"{'='*20}")
        print(" 1. Add Friend")
        print(" 2. Find Friend")
        print(" 3. Remove Friend")
        print(" 4. Show All Friends")
        print(" 5. Send Money to a Friend") 
        print(" 0. Go back")

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