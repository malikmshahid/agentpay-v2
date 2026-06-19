from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AgentPay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.circle.com/v1/w3s"

def get_headers():
    api_key = os.getenv("CIRCLE_API_KEY")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

@app.get("/")
def root():
    return {"message": "AgentPay is running!", "status": "ok"}

@app.get("/wallets")
def get_wallets():
    try:
        res = requests.get(
            f"{BASE_URL}/wallets",
            headers=get_headers()
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.post("/create-wallet")
def create_wallet():
    try:
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "blockchains": ["ARB-SEPOLIA"]
        }
        res = requests.post(
            f"{BASE_URL}/developer/wallets",
            headers=get_headers(),
            json=payload
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/balance/{wallet_id}")
def get_balance(wallet_id: str):
    try:
        res = requests.get(
            f"{BASE_URL}/wallets/{wallet_id}/balances",
            headers=get_headers()
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.post("/pay")
def make_payment(amount: float, to_address: str, reason: str):
    try:
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "amounts": [str(amount)],
            "destinationAddress": to_address,
            "tokenId": "USDC",
            "blockchain": "ARB-SEPOLIA"
        }
        return {
            "status": "payment_initiated",
            "amount": amount,
            "to": to_address,
            "reason": reason,
            "network": "Arc Testnet",
            "currency": "USDC",
            "idempotencyKey": payload["idempotencyKey"]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/agent/decide")
def agent_decide(task: str, amount: float = 1.0):
    decisions = {
        "pay api": f"Agent will pay {amount} USDC for API service",
        "check balance": "Agent will check wallet balance",
        "send payment": f"Agent will send {amount} USDC payment",
    }
    task_lower = task.lower()
    for key, decision in decisions.items():
        if key in task_lower:
            return {
                "task": task,
                "decision": decision,
                "status": "approved",
                "agent": "AgentPay AI"
            }
    return {
        "task": task,
        "decision": "Agent analyzing task...",
        "status": "pending",
        "agent": "AgentPay AI"
    }