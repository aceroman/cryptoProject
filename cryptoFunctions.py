import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def generateKey():
    key = Fernet.generate_key()
    with open(".env", "w") as envFile:
        envFile.write(f"SECRET_KEY={key.decode()}\n")
    
    load_dotenv()

def loadKey():
    key = os.getenv("SECRET_KEY")
    
    # if there isn't a key we'll generate one and load the new one in
    if key is None:
        generateKey()
        key = os.getenv("SECRET_KEY")
    return key.encode()


# initialzing our encryption
cipher = Fernet(loadKey())

# encrypting our password
def passwordEncryption(password):
    return cipher.encrypt(password.encode()).decode()

def passwordDecryption(passwordEncryption):
    return cipher.decrypt(passwordEncryption.encode()).decode()