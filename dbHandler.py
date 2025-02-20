import sqlite3
import bcrypt
from cryptoFunctions import passwordEncryption, passwordDecryption


def createTable():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS master_password (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       hashed_password TEXT NOT NULL
                   )
                   ''')
    conn.commit()
    conn.close()


def setMasterPassword():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM master_password")
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return
    
    master_password = input("Set a new master password: ")
    hashedPassword = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    
    cursor.execute('INSERT INTO master_password (hashed_password) VALUES (?)', (hashedPassword,))
    conn.commit()
    conn.close()
    print("You're master password was successfully set!")
    

def verifyMasterPassword():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT hashed_password FROM master_password")
    result = cursor.fetchone()
    
    if not result:
        print("No master password found.")
        conn.close()
        return False
    
    storedHashedPassword = result[0].encode() if isinstance(result[0], str) else result[0]
    conn.close()
    
    attempts = 3
    while attempts > 0:
        inputPassword = input("Enter master passsword: ")
        if bcrypt.checkpw(inputPassword.encode(), storedHashedPassword):
            print("Access Granted!")
            return True
        else:
            attempts -= 1
            print("Incorrect password. Try again")
    print("Too many failed attempts. Exiting program.")
    exit()

# storing my encrypted passwords
def storePasswords(website, username, password):
    encryptedPassword = passwordEncryption(password)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PASSWORDS (website, username, encrypted_password) VALUES(?, ?, ?)", (website, username, encryptedPassword))
    
    conn.commit()
    conn.close()

# getting our stored passwords from the database
def retrievePasswords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username FROM passwords ORDER BY LOWER(website) ASC")
    data = cursor.fetchall()
    conn.close()
    
    return data
        
# updating stored passwords
def updatePassword(website, username, newPassword):
    encryptedPassword = passwordEncryption(newPassword)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET encrypted_password = ? WHERE website = ? AND username = ?", (encryptedPassword, website, username))
    conn.commit()
    conn.close()


# Instead of showing the pass, I created a verification check
def checkPassword(website, username, inputPassword):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password FROM passwords WHERE website = ? AND username = ?", (website, username))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        storedHash = result[0]
        return passwordDecryption(storedHash) == inputPassword
    return False

# removing an entry from the database
def removeEntry(website, username):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE website = ? AND username = ?", (website, username))
    record = cursor.fetchone()
    
    if record:
        cursor.execute("DELETE FROM passwords WHERE website = ? AND username = ?", (website, username))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


createTable()