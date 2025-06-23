from web3 import Web3
import json
import os

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Your Ganache port
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Ensure connection works
if not web3.is_connected():
    raise Exception("⚠️ Web3 is not connected to Ganache")

# Load the compiled contract ABI
artifact_path = os.path.join(os.path.dirname(__file__), "build", "contracts", "FinanceLedger.json")
with open(artifact_path, "r") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Contract address after truffle migrate (replace with yours or read from file)
contract_address = "0xB4ecC923fd2be22aDE59a6C892FDDb1311f47B85"

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Set default account
web3.eth.default_account = web3.eth.accounts[0]
