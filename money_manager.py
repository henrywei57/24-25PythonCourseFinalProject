import json
import os

MONEY_FILE = "money_data.json"

def save_money(balance):
    """Save the current balance to a file"""
    data = {"balance": balance}
    with open(MONEY_FILE, 'w') as f:
        json.dump(data, f)

def load_money():
    """Load the balance from file, return 1000 if file doesn't exist"""
    try:
        if os.path.exists(MONEY_FILE):
            with open(MONEY_FILE, 'r') as f:
                data = json.load(f)
                return data.get("balance", 1000)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return 1000  # Default starting balance 