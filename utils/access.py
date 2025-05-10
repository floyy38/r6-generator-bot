import time
import json
import os

PREMIUM_FILE = "data/premium_users.json"

def load_premium():
    if os.path.exists(PREMIUM_FILE):
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    return {}

premium_users = load_premium()

def has_active_premium(user_id):
    user_id = str(user_id)
    if user_id not in premium_users:
        return False
    expiry = premium_users[user_id]
    return expiry == "lifetime" or expiry > time.time()

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f)

