# 📊 Social Media Analytics Dashboard

A full-stack AI-powered social media analytics dashboard that scrapes live Instagram and LinkedIn profiles, compares competitors, visualizes engagement data, and generates intelligent insights using Google Gemini AI.

---

## 🚀 Live Features

- 🔍 Live Profile Scraping — Fetch real-time Instagram & LinkedIn data via RapidAPI
- ⚔️ Competitor Analysis — Scrape multiple profiles and compare side-by-side
- 📈 Interactive Charts — Follower comparison, engagement rate, radar chart, growth trend
- 🤖 Gemini AI Insights — Strengths, content gaps, best posting times, growth strategy
- 📄 PDF Export — Download full analytics report
- 🔄 Mock Fallback — Demo data loads instantly if API quota exceeded

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Recharts |
| Backend | Python, Flask, Flask-CORS |
| Scraping | RapidAPI (Instagram Bulk Scraper, LinkedIn Scraper) |
| AI | Google Gemini 1.5 Flash |
| PDF | ReportLab |
| Data | JSON (mock), MongoDB-ready |

---

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- RapidAPI account (free tier works)
- Google Gemini API key (free tier works)

---
2. Backend Setup
   cd backend
    pip install -r requirements.txt

Create a .env file in the backend/ folder:
- RAPIDAPI_KEY=your_rapidapi_key_here
- GEMINI_API_KEY=your_gemini_api_key_here

Start the Flask server:
- python app.py
- Backend runs at → http://localhost:5000


3. Frontend Setup
  - cd frontend
  - npm install
  - npm run dev
 
 
4. How to Use
- Open http://localhost:5173

- In "Scrape Live Profile" — enter an Instagram username (e.g. netflix) → click Scrape

- First scraped profile becomes your main profile

- Scrape more profiles → they become competitors

- Go to Charts tab → see live comparison charts

- Go to AI Insights tab → click Generate Insights

- Click Export PDF to download the full report


📝 Notes
- Instagram API does not expose likes/comments on free tier — engagement is estimated based on follower count using industry benchmarks

- LinkedIn post metrics are unavailable on free tier — engagement is estimated based on follower size and headline category

- Mock data loads by default so the dashboard is always demo-ready even without API keys
   




