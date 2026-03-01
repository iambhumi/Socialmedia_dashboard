from pymongo import MongoClient

# Local MongoDB — no password needed
MONGO_URI = "mongodb://localhost:27017"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = client["social_dashboard"]
    db.command("ping")
    print("✅ Local MongoDB connected!")
except Exception as e:
    print(f"❌ Failed: {e}")
