import hashlib
import getpass
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("CONTROLLER_USERNAME")
PASSWORD_HASH = os.getenv("CONTROLLER_PASSWORD_HASH")

def verify_login():
    print("[LOGIN] Controller access required.")
    input_user = input("Username: ")
    input_pass = getpass.getpass("Password: ")
    
    hashed_input = hashlib.sha256(input_pass.encode()).hexdigest()

    if input_user == USERNAME and hashed_input == PASSWORD_HASH:
        print("[ACCESS GRANTED]")
        return True
    else:
        print("[ACCESS DENIED]")
        return False