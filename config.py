import json

BOT_TOKEN = "YOUR_BOT_TOKEN"
DB_NAME = "crypto.db"

with open('intervals.json', 'r', encoding='utf-8') as file:
  INTERVALS_NAMES = json.load(file)