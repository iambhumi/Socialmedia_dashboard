from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=ENV_PATH, override=True)

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://bhumi:bhumi1234@cluster0.p4fkm.mongodb.net/social_dashboard?retryWrites=true&w=majority&appName=Cluster0")
print(f" MONGO_URI being used = {MONGO_URI}")

# ── Try to connect 
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = client["Social_dashboard"]
    client.admin.command("ping")
    profiles_collection = db["profiles"]
    snapshots_collection = db["snapshots"]
    DB_CONNECTED = True
    print(" MongoDB connected!")
except Exception as e:
    print(f" MongoDB not connected — running without DB: {e}")
    DB_CONNECTED = False
    profiles_collection = None
    snapshots_collection = None


def save_profile(profile_data):
    if not DB_CONNECTED or profiles_collection is None:
        print(" DB not available — skipping save")
        return None
    try:
        profile_data["updated_at"] = datetime.utcnow().isoformat()
        result = profiles_collection.update_one(
            {
                "username": profile_data["username"],
                "platform": profile_data["platform"]
            },
            {"$set": profile_data},
            upsert=True
        )
        snapshot = {
            "username": profile_data["username"],
            "platform": profile_data["platform"],
            "followers": profile_data.get("followers", 0),
            "engagement_rate": profile_data.get("engagement_rate", 0),
            "total_posts": profile_data.get("total_posts", 0),
            "timestamp": datetime.utcnow().isoformat(),
            "date": datetime.utcnow().strftime("%b %Y")
        }
        snapshots_collection.insert_one(snapshot)
        print(f" Saved {profile_data['username']} to DB")
        return result.upserted_id
    except Exception as e:
        print(f" Save failed — skipping: {e}")
        return None


def get_all_profiles():
    if not DB_CONNECTED or profiles_collection is None:
        return []
    try:
        return list(profiles_collection.find({}, {"_id": 0}))
    except Exception as e:
        print(f" get_all_profiles failed: {e}")
        return []


def get_profile(username, platform):
    if not DB_CONNECTED or profiles_collection is None:
        return None
    try:
        return profiles_collection.find_one(
            {"username": username, "platform": platform},
            {"_id": 0}
        )
    except Exception as e:
        print(f" get_profile failed: {e}")
        return None


def get_growth_history(username, platform):
    if not DB_CONNECTED or snapshots_collection is None:
        return []
    try:
        return list(snapshots_collection.find(
            {"username": username, "platform": platform},
            {"_id": 0, "followers": 1, "date": 1, "timestamp": 1}
        ).sort("timestamp", 1).limit(12))
    except Exception as e:
        print(f" get_growth_history failed: {e}")
        return []


def delete_profile(username, platform):
    if not DB_CONNECTED or profiles_collection is None:
        return False
    try:
        profiles_collection.delete_one({"username": username, "platform": platform})
        snapshots_collection.delete_many({"username": username, "platform": platform})
        return True
    except Exception as e:
        print(f" delete_profile failed: {e}")
        return False


def get_competitors():
    if not DB_CONNECTED or profiles_collection is None:
        return []
    try:
        return list(profiles_collection.find({"type": "competitor"}, {"_id": 0}))
    except Exception as e:
        print(f" get_competitors failed: {e}")
        return []
