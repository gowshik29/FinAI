
# from blockchain_layer.web3_config import web3, contract
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Optional: Enable CORS if your frontend is on a different port (e.g., Streamlit on :8501)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:8501"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/add_transaction")
# def add_transaction(data: dict):
#     tx = contract.functions.logTransaction(
#         data["id"], data["purpose"], data["amount"]
#     ).transact()
#     receipt = web3.eth.wait_for_transaction_receipt(tx)
#     return {"txHash": receipt.transactionHash.hex()}


from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3
import json
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Enable CORS for frontend JS access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Web3 Setup ---
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
if not w3.is_connected():
    raise Exception("⚠️ Web3 connection to Ganache failed.")

# Load Smart Contract
contract_path = Path("blockchain_layer/build/contracts/FinanceLedger.json")
if not contract_path.exists():
    raise Exception("⚠️ Contract JSON not found. Compile with Truffle first.")

with contract_path.open() as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Replace this with the correct deployed contract address
contract_address = Web3.to_checksum_address("0xB4ecC923fd2be22aDE59a6C892FDDb1311f47B85")
contract = w3.eth.contract(address=contract_address, abi=abi)

# Use a funded Ganache account (replace private key securely in production)
default_account = w3.eth.accounts[0]
private_keys = {
    w3.eth.accounts[0]: "0xfb2be2f6ed3ed84e8ad35392ff451b63864fc26b8ebde9b20752da637117d81c"  # Update this!
}

# --- HTML Page ---
@app.get("/", response_class=HTMLResponse)
async def load_form(request: Request):
    return templates.TemplateResponse("transaction_form.html", {"request": request})


# --- Add Transaction ---
@app.post("/add_transaction")
async def add_transaction(id: int = Form(...), purpose: str = Form(...), amount: int = Form(...)):
    try:
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        nonce = w3.eth.get_transaction_count(default_account)
        tx = contract.functions.addTransaction(id, purpose, amount).build_transaction({
            'from': default_account,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_keys[default_account])
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return {
            "status": "success",
            "message": "Transaction submitted successfully",
            "transaction_hash": tx_hash.hex()
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


# --- Get All Transactions ---
@app.get("/transactions")
async def get_transactions():
    try:
        count = contract.functions.getTransactionCount().call()
        transactions = []
        for i in range(count):
            tx = contract.functions.getTransaction(i).call()
            transactions.append({
                "id": tx[0],
                "purpose": tx[1],
                "amount": tx[2],
                "timestamp": tx[3],
            })
        return {"transactions": transactions}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
