import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone

load_dotenv()

url = os.getenv("MONGO_URI")
client = MongoClient(url)
db = client['crypto_db']
collection = db['prices']

def insert_price(bitcoin, ethereum):
    doc = {
        "bitcoin": float(bitcoin),
        "ethereum": float(ethereum),
        "updated_at": datetime.now(timezone.utc),
    }
    collection.insert_one(doc)

def get_all_prices():
    return list(collection.find({}, {"_id": 0}))

