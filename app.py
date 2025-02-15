from dbHandler import storePasswords, retrievePasswords, updatePassword, checkPassword, removeEntry


def main():
    while True:
        print("\n Welcome to my Secure Password Manager")
        print("1. Store a new password")
        print("2. View current saved passwords")
        print("3. Verify a stored password")
        print("4. Update a password")
        print("5. Remove a password")
        print("6. Exit the program")
        
        
        choice = input("Please select the following: \n")
        
        # Option 1
        if choice == "1":
            website = input("Enter the name of the website: ")
            username = input("Enter the username of the website: ")
            password = input("Please type in the password: ")
            storePasswords(website, username, password)
            print("This password has been stored securely!")
        
        # Option 2
        elif choice == "2":
            passwords = retrievePasswords()
            if not passwords:
                print("No passwords are currently stored.")
            else:
                print("\n Current Saved Passwords in your database")
                for website, username, in passwords:
                    print(f"Website: {website} | Username: {username} ")
        
        # Option 3
        elif choice == "3":
            website = input("Enter website: \n")
            username = input("Enter the username: \n")
            inputPassword = input("Enter password to verify: ")
            
            if checkPassword(website, username, inputPassword):
                print("Password Matches!")
            else:
                print("Incorrect password or account not found")
        
        # Option 4
        elif choice == "4":
            website = input("Enter website: \n")
            username = input("Enter the username: \n")
            newPassword = input("Enter the new password: \n")
            
            updatePassword(website, username, newPassword)
            print("Password updated successfully!")

        # Option 5        
        elif choice == "5":
            website = input("Enter website: \n")
            username = input("Enter the username: \n")
            
            if removeEntry(website, username):
                print("Password entry removed successfully!")
            else:
                print("No matching record found. Double check your input.")
            
        # Option 6
        elif choice == "6":
            print("Exiting your password manager!")
            break
        else:
            print("Invalid option. Please select one of the options.")


if __name__ == '__main__':
    main()