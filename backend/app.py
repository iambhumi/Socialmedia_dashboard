from pdf_service import generate_pdf_report
from flask import send_file

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from gemini_service import generate_insights

app = Flask(__name__)
CORS(app)

# Load mock data
def load_data():
    with open('mock_data.json', 'r') as f:
        return json.load(f)

# GET all profiles
@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    data = load_data()
    return jsonify(data)

# GET main profile only
@app.route('/api/profiles/main', methods=['GET'])
def get_main_profile():
    data = load_data()
    main = next((p for p in data if p['type'] == 'main'), None)
    return jsonify(main)

# GET competitors only
@app.route('/api/profiles/competitors', methods=['GET'])
def get_competitors():
    data = load_data()
    competitors = [p for p in data if p['type'] == 'competitor']
    return jsonify(competitors)

# GET AI insights
@app.route('/api/insights', methods=['GET'])
def get_insights():
    data = load_data()
    main = next((p for p in data if p['type'] == 'main'), None)
    competitors = [p for p in data if p['type'] == 'competitor']
    insights = generate_insights(main, competitors)
    return jsonify({"insights": insights})

# GET engagement comparison data
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

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    try:
        data = load_data()
        insights_data = generate_insights(
            next(p for p in data if p['type'] == 'main'),
            [p for p in data if p['type'] == 'competitor']
        )
        path = generate_pdf_report(data, insights_data)
        return send_file(
            path,
            as_attachment=True,
            download_name='ArivuPro_Analytics_Report.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
