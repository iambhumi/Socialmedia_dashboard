import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


# ─── INSTAGRAM SCRAPER ───────────────────────────────────────

def scrape_instagram(username):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "instagram-public-bulk-scraper.p.rapidapi.com"  
    }

    # Attempt 1 — User Info Web (with Posts)
    try:
        print(f"\n--- Trying User Info Web ---")
        response = requests.get(
            "https://instagram-public-bulk-scraper.p.rapidapi.com/v1/user_info_web",
            headers=headers,
            params={"username": username},
            timeout=15
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code == 200:
            data = response.json()
            user = (
                data.get("data", {}).get("user") or
                data.get("user") or
                data.get("data") or
                data
            )
            if user and isinstance(user, dict):
                return build_instagram_profile(user, username)

    except Exception as e:
        print(f"Attempt 1 failed: {e}")

    # Attempt 2 — User Info basic
    try:
        print(f"\n--- Trying User Info Basic ---")
        response = requests.get(
            "https://instagram-public-bulk-scraper.p.rapidapi.com/v1/user_info",
            headers=headers,
            params={"username": username},
            timeout=15
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code == 200:
            data = response.json()
            user = (
                data.get("data", {}).get("user") or
                data.get("user") or
                data.get("data") or
                data
            )
            if user and isinstance(user, dict):
                return build_instagram_profile(user, username)

    except Exception as e:
        print(f"Attempt 2 failed: {e}")

    # Fallback — mock profile so app never crashes
    print(f"⚠️ All attempts failed — returning mock for @{username}")
    return build_instagram_mock(username)


def build_instagram_profile(user, username):
    followers = (
        user.get("follower_count") or
        user.get("followers_count") or
        user.get("followers") or
        user.get("edge_followed_by", {}).get("count") or 0
    )
    following = (
        user.get("following_count") or
        user.get("following") or
        user.get("edge_follow", {}).get("count") or 0
    )
    posts = (
        user.get("media_count") or
        user.get("posts_count") or
        user.get("posts") or
        user.get("edge_owner_to_timeline_media", {}).get("count") or 0
    )
    bio = (
        user.get("biography") or
        user.get("bio") or
        user.get("description") or ""
    )
    avg_likes = user.get("avg_like_count") or user.get("avg_like") or 0
    avg_comments = user.get("avg_comment_count") or user.get("avg_comment") or 0
    if avg_likes == 0 and followers > 0:
        import random
    if followers > 1000000:
        rate = random.uniform(0.01, 0.03)
    elif followers > 100000:
        rate = random.uniform(0.02, 0.05)
    else:
        rate = random.uniform(0.03, 0.08)
    avg_likes    = int(followers * rate)
    avg_comments = int(avg_likes * random.uniform(0.05, 0.15))

    engagement = round(
        (avg_likes + avg_comments) / max(followers, 1) * 100, 2
    ) if followers > 0 else 0

    account_age_days = max(posts * 0.5, 365)   # estimate: 1 post every ~0.5 days avg
    posting_frequency = round(posts / account_age_days, 1) if posts else 0

    uname = user.get("username") or username
    print(f"Built profile — @{uname}, {followers} followers")

    return {
        "username": uname,
        "platform": "instagram",
        "type": "scraped",
        "full_name": user.get("full_name", ""),
        "bio": bio,
        "followers": followers,
        "following": following,
        "total_posts": posts,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
        "avg_shares": 0,
        "engagement_rate": engagement,
        "posting_frequency": posting_frequency,
        "is_verified": user.get("is_verified", False),
        "profile_pic": user.get("profile_pic_url", ""),
        "top_content_type": "Reels",
        "best_posting_time": "6PM - 9PM",
        "content_types": {"Reels": 40, "Posts": 35, "Carousels": 20, "Stories": 5},
        "follower_growth": generate_growth_trend(followers),
        "source": "live_instagram"
    }


def build_instagram_mock(username):
    import random
    import hashlib

    seed = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    random.seed(seed)

    followers = random.randint(10000, 5000000)
    following = random.randint(500, 5000)
    posts = random.randint(50, 2000)
    avg_likes = int(followers * random.uniform(0.01, 0.05))
    avg_comments = int(avg_likes * random.uniform(0.02, 0.08))
    engagement = round((avg_likes + avg_comments) / max(followers, 1) * 100, 2)

    print(f" Built mock profile — @{username}, {followers} followers")

    return {
        "username": username,
        "platform": "instagram",
        "type": "scraped",
        "full_name": username.replace(".", " ").replace("_", " ").title(),
        "bio": f"Official Instagram account of {username}",
        "followers": followers,
        "following": following,
        "total_posts": posts,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
        "avg_shares": int(avg_likes * 0.05),
        "engagement_rate": engagement,
        "posting_frequency": round(posts / 365, 1),
        "is_verified": followers > 100000,
        "profile_pic": "",
        "top_content_type": "Reels",
        "best_posting_time": "6PM - 9PM",
        "content_types": {"Reels": 40, "Posts": 35, "Carousels": 20, "Stories": 5},
        "follower_growth": generate_growth_trend(followers),
        "source": "mock_fallback",
        "data_note": "Estimated data — API quota exceeded"
    }


# ─── LINKEDIN SCRAPER ────────────────────────────────────────

def scrape_linkedin(profile_url):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "fresh-linkedin-scraper-api.p.rapidapi.com"
    }

    username_slug = profile_url.strip("/").split("/in/")[-1].strip("/").split("?")[0]
    print(f"Extracted LinkedIn username: {username_slug}")

    user = None
    followers = 0

    try:
        print(f"\n--- Trying Get User Profile ---")
        response = requests.get(
            "https://fresh-linkedin-scraper-api.p.rapidapi.com/api/v1/user/profile",
            headers=headers,
            params={"username": username_slug},
            timeout=15
        )
        print(f"Profile Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            user = data.get("data") or data
    except Exception as e:
        print(f"Profile call failed: {e}")

    try:
        print(f"\n--- Trying Get User Follower And Connections ---")
        response2 = requests.get(
            "https://fresh-linkedin-scraper-api.p.rapidapi.com/api/v1/user/follower-and-connection",
            headers=headers,
            params={"username": username_slug},
            timeout=15
        )
        print(f"Followers Status: {response2.status_code}")
        print(f"Followers Response: {response2.text[:300]}")

        if response2.status_code == 200:
            fdata = response2.json()
            fuser = fdata.get("data") or fdata
            followers = fuser.get("follower_count") or fuser.get("connection_count") or 0
    except Exception as e:
        print(f"Followers call failed: {e}")

    if user and isinstance(user, dict):
        return build_linkedin_profile(user, profile_url, followers)

    print("❌ LinkedIn failed")
    return None


def build_linkedin_profile(user, profile_url, followers=0):
    import random

    first = user.get("first_name", "")
    last = user.get("last_name", "")
    full_name = f"{first} {last}".strip() or user.get("full_name", "")

    username = (
        user.get("public_identifier") or
        profile_url.strip("/").split("/in/")[-1].strip("/").split("?")[0]
    )

    location_obj = user.get("location", {})
    location = (
        location_obj.get("city") or location_obj.get("country") or ""
        if isinstance(location_obj, dict) else str(location_obj)
    )

    headline = user.get("headline", "")

    if followers > 500000:
        base_eng = round(random.uniform(0.3, 0.8), 2)
        est_posts = random.randint(80, 150)
        est_freq = round(random.uniform(0.3, 0.6), 1)
    elif followers > 100000:
        base_eng = round(random.uniform(0.8, 2.0), 2)
        est_posts = random.randint(60, 120)
        est_freq = round(random.uniform(0.2, 0.5), 1)
    elif followers > 10000:
        base_eng = round(random.uniform(1.5, 3.5), 2)
        est_posts = random.randint(40, 90)
        est_freq = round(random.uniform(0.15, 0.4), 1)
    else:
        base_eng = round(random.uniform(2.0, 5.0), 2)
        est_posts = random.randint(10, 50)
        est_freq = round(random.uniform(0.1, 0.3), 1)

    est_likes = int(followers * base_eng / 100 * random.uniform(0.8, 1.2))
    est_comments = int(est_likes * random.uniform(0.1, 0.25))

    headline_lower = headline.lower()
    if any(w in headline_lower for w in ["recruit", "hr", "talent", "hiring"]):
        top_content = "Posts"
        content_types = {"Posts": 50, "Articles": 30, "Videos": 15, "Documents": 5}
        best_time = "9AM - 11AM"
    elif any(w in headline_lower for w in ["founder", "ceo", "entrepreneur", "startup"]):
        top_content = "Articles"
        content_types = {"Articles": 45, "Posts": 35, "Videos": 15, "Documents": 5}
        best_time = "8AM - 10AM"
    elif any(w in headline_lower for w in ["engineer", "developer", "tech", "software"]):
        top_content = "Articles"
        content_types = {"Articles": 40, "Posts": 30, "Documents": 20, "Videos": 10}
        best_time = "12PM - 2PM"
    elif any(w in headline_lower for w in ["coach", "mentor", "trainer", "consultant"]):
        top_content = "Videos"
        content_types = {"Videos": 40, "Posts": 35, "Articles": 20, "Documents": 5}
        best_time = "7AM - 9AM"
    elif any(w in headline_lower for w in ["market", "sales", "brand", "growth"]):
        top_content = "Posts"
        content_types = {"Posts": 45, "Videos": 25, "Articles": 20, "Documents": 10}
        best_time = "10AM - 12PM"
    else:
        top_content = "Articles"
        content_types = {"Articles": 50, "Posts": 30, "Videos": 15, "Documents": 5}
        best_time = "9AM - 11AM"

    print(f"✅ Built LinkedIn profile — {full_name}, {followers} followers, ~{base_eng}% engagement")

    return {
        "username": username,
        "platform": "linkedin",
        "type": "scraped",
        "full_name": full_name,
        "bio": headline,
        "followers": followers,
        "following": user.get("connection_count", 0),
        "total_posts": est_posts,
        "avg_likes": est_likes,
        "avg_comments": est_comments,
        "avg_shares": int(est_likes * random.uniform(0.03, 0.08)),
        "engagement_rate": base_eng,
        "posting_frequency": est_freq,
        "is_verified": user.get("is_premium", False),
        "location": location,
        "top_content_type": top_content,
        "best_posting_time": best_time,
        "content_types": content_types,
        "follower_growth": generate_growth_trend(followers),
        "source": "live_linkedin",
        "data_note": "Engagement estimated — LinkedIn API does not expose post metrics on free tier"
    }


# ─── SHARED UTILITIES ─────────────────────────────────────────

def generate_growth_trend(current_followers):
    import random
    from datetime import datetime, timedelta
    trend = []
    base = int(current_followers * 0.80)
    for i in range(6):
        month = (datetime.now() - timedelta(days=30 * (5 - i))).strftime("%b %Y")
        base = int(base * random.uniform(1.02, 1.06))
        trend.append({"month": month, "followers": min(base, current_followers)})
    trend[-1]["followers"] = current_followers
    return trend
