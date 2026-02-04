import getpass
from eth_account import Account
from pathlib import Path
import json

KEYSTORE_PATH = Path(".keystore.json")

def main():
    private_key = getpass.getpass("Enter your private key:")
    my_account = Account.from_key(private_key)
    password = getpass.getpass("Enter a password to encrypt") #greeting on phone
    encrypted_account = Account.encrypt(private_key, password)

    with open(KEYSTORE_PATH, "w") as keystore_file:
        json.dump(encrypted_account, keystore_file)
    print(f"Encrypted key saved to {KEYSTORE_PATH}")

if __name__ == "__main__":
    main()