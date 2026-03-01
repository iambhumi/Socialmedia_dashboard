from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os

from scraper import scrape_instagram, scrape_linkedin
from gemini_service import generate_insights
from pdf_service import generate_pdf_report
from database import (
    save_profile,
    get_all_profiles,
    get_profile,
    get_growth_history,
    delete_profile
)

load_dotenv()

app = Flask(__name__)
CORS(app)


# ── Load mock data helper ─────────────────────────────────────
def load_data():
    with open('mock_data.json', 'r') as f:
        return json.load(f)



# GET all mock profiles
@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    data = load_data()
    return jsonify(data)


# GET main mock profile only
@app.route('/api/profiles/main', methods=['GET'])
def get_main_profile():
    data = load_data()
    main = next((p for p in data if p['type'] == 'main'), None)
    return jsonify(main)


# GET mock competitors only
@app.route('/api/profiles/competitors', methods=['GET'])
def get_competitors():
    data = load_data()
    competitors = [p for p in data if p['type'] == 'competitor']
    return jsonify(competitors)


# GET comparison data (for charts)
@app.route('/api/comparison', methods=['GET'])
def get_comparison():
    data = load_data()
    comparison = []
    for profile in data:
        comparison.append({
            "username": profile['username'],
            "followers": profile['followers'],
            "engagement_rate": profile['engagement_rate'],
            "avg_likes": profile['avg_likes'],
            "posting_frequency": profile['posting_frequency']
        })
    return jsonify(comparison)



#  LIVE SCRAPING ROUTES

# Scrape Instagram live
@app.route('/api/scrape/instagram/<username>', methods=['GET'])
def scrape_instagram_profile(username):
    result = scrape_instagram(username)
    if result:
        save_profile(result)     #  Save to MongoDB
        return jsonify(result)
    return jsonify({"error": "Failed to scrape — check username or API key"}), 400


# Scrape LinkedIn live
@app.route('/api/scrape/linkedin', methods=['POST'])
def scrape_linkedin_profile():
    body = request.get_json()
    url = body.get('url')
    if not url:
        return jsonify({"error": "LinkedIn URL required"}), 400
    result = scrape_linkedin(url)
    if result:
        save_profile(result)     # Save to MongoDB
        return jsonify(result)
    return jsonify({"error": "Failed to scrape — check URL or API key"}), 400


# Scrape competitor (used by CompetitorPanel.jsx)
@app.route('/api/competitor', methods=['POST'])
def scrape_competitor():
    data = request.json
    platform = data.get('platform', '').lower()
    identifier = data.get('identifier', '').strip()

    if not platform or not identifier:
        return jsonify({"error": "platform and identifier required"}), 400

    try:
        if platform == 'instagram':
            result = scrape_instagram(identifier)
        elif platform == 'linkedin':
            result = scrape_linkedin(identifier)
        else:
            return jsonify({"error": "Unsupported platform"}), 400

        if result:
            result['type'] = 'competitor'    #  Mark as competitor
            save_profile(result)             #  Save to MongoDB
            return jsonify({"success": True, "data": result})
        else:
            return jsonify({"error": "Could not fetch competitor data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Scrape multiple profiles + analyze with Gemini
@app.route('/api/scrape/analyze', methods=['POST'])
def scrape_and_analyze():
    body = request.get_json()
    profiles_to_scrape = body.get('profiles', [])

    scraped = []
    for p in profiles_to_scrape:
        result = None
        if p['platform'] == "instagram":
            result = scrape_instagram(p['id'])
        elif p['platform'] == "linkedin":
            result = scrape_linkedin(p['id'])

        if not result:
            return jsonify({"error": f"Failed to scrape profile {p['id']}"}), 400

        save_profile(result)     
        scraped.append(result)

    if len(scraped) < 2:
        return jsonify({"error": "Need at least 2 profiles to analyze"}), 400

    main = scraped[0]
    competitors = scraped[1:]
    insights = generate_insights(main, competitors)

    return jsonify({
        "profiles": scraped,
        "insights": insights
    })





# POST — Generate Gemini AI insights
@app.route('/api/insights', methods=['POST'])
def get_insights():
    data = request.json
    user_profile = data.get('user_profile', {})
    competitor_profiles = data.get('competitor_profiles', [])

    if not user_profile:
        return jsonify({"error": "user_profile is required"}), 400

    insights = generate_insights(user_profile, competitor_profiles)
    return jsonify({"success": True, "insights": insights})



#  DATABASE ROUTES

# GET all profiles saved in MongoDB
@app.route('/api/saved-profiles', methods=['GET'])
def get_saved_profiles():
    profiles = get_all_profiles()
    return jsonify(profiles)


# GET real growth history for a profile from DB snapshots
@app.route('/api/growth/<platform>/<username>', methods=['GET'])
def get_growth(platform, username):
    history = get_growth_history(username, platform)
    return jsonify(history)


# DELETE a saved profile from DB
@app.route('/api/profile/<platform>/<username>', methods=['DELETE'])
def remove_profile(platform, username):
    delete_profile(username, platform)
    return jsonify({"success": True, "message": f"Deleted {username} from {platform}"})


# 
#  EXPORT ROUTE


# Export PDF — uses live DB data if available, else mock
@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    try:
        
        body = request.get_json(silent=True) or {}
        profiles = body.get('profiles', [])
        insights_text = body.get('insights', '')
        
        # Fallback to mock if no live data sent
        if not profiles:
            profiles = load_data()
        
        if not profiles:
            return jsonify({"error": "No profile data available"}), 400

        # Generate insights if not provided
        if not insights_text:
            main = next((p for p in profiles if p.get('type') == 'main'), profiles[0])
            competitors = [p for p in profiles if p.get('type') == 'competitor']
            insights_text = generate_insights(main, competitors)

        path = generate_pdf_report(profiles, insights_text)
        return send_file(
            path,
            as_attachment=True,
            download_name='ArivuPro_Analytics_Report.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"PDF error: {e}")
        return jsonify({"error": str(e)}), 500
           

        


#  CSV EXPORT ROUTE

@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    import csv
    import io
    data = request.json.get('profiles', [])
    if not data:
        return jsonify({"error": "No profiles data provided"}), 400

    fields = [
        "username", "platform", "type", "full_name",
        "followers", "following", "total_posts",
        "engagement_rate", "avg_likes", "avg_comments",
        "posting_frequency", "bio", "location",
        "top_content_type", "best_posting_time", "source"
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)

    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=social_report.csv'
    }



if __name__ == '__main__':
    app.run(debug=True, port=5000)
