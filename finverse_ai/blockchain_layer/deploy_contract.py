# File: blockchain_layer/deploy_contract.py
import json
from web3 import Web3
import os

GANACHE_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Load compiled contract
contract_path = os.path.join(os.path.dirname(__file__), "..", "build", "contracts", "FinanceLedger.json")
with open(contract_path) as f:
    contract_json = json.load(f)

abi = contract_json["abi"]
bytecode = contract_json["bytecode"]

# Deploy contract
account = w3.eth.accounts[0]
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress

# Save address to file
with open("blockchain_layer/contract_address.txt", "w") as f:
    f.write(contract_address)

print(f"Contract deployed at: {contract_address}")
