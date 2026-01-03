from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017")
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