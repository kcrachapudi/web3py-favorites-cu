from eth_typing import Address
from vyper import compile_code
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
from encrypt_key import KEYSTORE_PATH
import getpass
from eth_account import Account
import json

network = {
    "rpc_url": "",
    "chain_id": 0,
    "currency_symbol": "",
    "address": ""
}

def Load_Network_Details(selected_Network: str, network:dict = network) -> bool :
    Networks = json.loads(open("Networks.json").read())
    net_found = False
    for net in Networks:
        if selected_Network == net:
            network["rpc_url"] = Networks[net]["rpc_url"]
            network["chain_id"] = Networks[net]["chain_id"]
            network["currency_symbol"] = Networks[net]["currency_symbol"]
            network["address"] = Networks[net]["address"]    
            net_found = True
            break
    return net_found

def main():
    print("Let's read in the Vyper code and deploy it!")

    GetSelectedNetwork = input("Enter the network you want to deploy to (e.g., Sepolia): ")
    if not Load_Network_Details(GetSelectedNetwork):
        print(f"Failed to load network details for '{GetSelectedNetwork}'")
        return
    with open("favorites.vy", "r") as fav_file:
        favorites_code = fav_file.read()
    compilation_details = compile_code(favorites_code, output_formats=["bytecode", "abi"])
    print("Compilation details:", compilation_details)

    w3 = Web3(HTTPProvider(network["rpc_url"]))
    fav_contract = w3.eth.contract(bytecode = compilation_details["bytecode"], abi = compilation_details["abi"]) 
    print("Favorite contract Deployed ", fav_contract)

    # Building a Transaction
    txn = fav_contract.constructor().build_transaction(
    {
        "from":  network["address"],
        "nonce": w3.eth.get_transaction_count(network["address"]),
        "gasPrice": w3.eth.gas_price,
        "chainId": network["chain_id"],
        "currencySymbol": network["currency_symbol"]
    })
    #print("Transaction details:", txn)
    print("Transaction From:", txn["from"])
    print("Transaction Nonce:", txn["nonce"])
    print("Transaction Gas Price:", txn["gasPrice"])
    print("Transaction Gas:", txn["gas"])
    print("Transaction Chain ID:", txn.get("chainId", "Not Specified"))

    # Signing a Transaction
    private_key = decrypt_key()
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    print("Signed Transaction:", signed_txn)

    # Sending a Transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Transaction Hash:", tx_hash.hex())
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction Receipt:", tx_receipt)   
    print(f'Done! Contract deployed at address: {tx_receipt.contractAddress}')

def decrypt_key()->str:
    with open(KEYSTORE_PATH, "r") as keystore_file:
        encrypted_account = json.load(keystore_file)
        password = getpass.getpass("Enter your password to decrypt the key:")
        key = Account.decrypt(encrypted_account, password)
        return key

if __name__ == "__main__":
    main()
