from vyper import compile_code
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os

load_dotenv()
Anvil_Private_Key_0 = os.getenv("Anvil_Private_Key_0")
RPC_URL = os.getenv("RPC_URL")

def main():
    print("Let's read in the Vyper code and deploy it!")
    with open("favorites.vy", "r") as fav_file:
        favorites_code = fav_file.read()
    compilation_details = compile_code(favorites_code, output_formats=["bytecode", "abi"])
    print("Compilation details:", compilation_details)

    w3 = Web3(HTTPProvider("http://localhost:8545"))
    fav_contract = w3.eth.contract(bytecode = compilation_details["bytecode"], abi = compilation_details["abi"]) 
    print("Favorite contract Deployed ", fav_contract)

    # Building a Transaction
    txn = fav_contract.constructor().build_transaction(
    {
        "from": w3.eth.accounts[0],
        "nonce": w3.eth.get_transaction_count(w3.eth.accounts[0]),
        "gasPrice": w3.eth.gas_price,
    })
    #print("Transaction details:", txn)
    print("Transaction From:", txn["from"])
    print("Transaction Nonce:", txn["nonce"])
    print("Transaction Gas Price:", txn["gasPrice"])
    print("Transaction Gas:", txn["gas"])
    print("Transaction Chain ID:", txn.get("chainId", "Not Specified"))

    # Signing a Transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=Anvil_Private_Key_0)
    print("Signed Transaction:", signed_txn)

if __name__ == "__main__":
    main()
