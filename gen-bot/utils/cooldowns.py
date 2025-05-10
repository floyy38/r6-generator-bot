import time
import json
import os

COOLDOWN_FILE = "data/cooldowns.json"
CUSTOM_COOLDOWN_FILE = "data/custom_cooldowns.json"

DEFAULT_COOLDOWNS = {
    "free": 600,
    "premium": 600
}

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

# Load cooldown and custom values
cooldowns = load_json(COOLDOWN_FILE)
custom_cooldowns = load_json(CUSTOM_COOLDOWN_FILE)

def get_cooldown_seconds(user_id, tier):
    user_id = str(user_id)
    if user_id in custom_cooldowns and tier in custom_cooldowns[user_id]:
        return custom_cooldowns[user_id][tier]
    return DEFAULT_COOLDOWNS[tier]

def check_cooldown(user_id, tier):
    now = time.time()
    user_id = str(user_id)
    last = cooldowns.get(user_id, {}).get(tier, 0)
    cooldown_time = get_cooldown_seconds(user_id, tier)
    return now - last >= cooldown_time

def update_cooldown(user_id, tier):
    now = time.time()
    user_id = str(user_id)
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    cooldowns[user_id][tier] = now
    save_json(COOLDOWN_FILE, cooldowns)

def set_custom_cooldown(user_id, tier, seconds):
    user_id = str(user_id)
    if user_id not in custom_cooldowns:
        custom_cooldowns[user_id] = {}
    custom_cooldowns[user_id][tier] = seconds
    save_json(CUSTOM_COOLDOWN_FILE, custom_cooldowns)
