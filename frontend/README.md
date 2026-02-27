# 📊 Social Media Analytics & Competitor Intelligence Dashboard

A web-based dashboard built for **ArivuPro** that tracks social media 
performance and compares it with competitors using AI-powered insights.

---

## 🚀 Features

- **Profile Analytics** — Follower growth, engagement rate, post performance
- **Competitor Analysis** — Side-by-side comparison of 4-5 profiles
- **AI Insights** — Gemini AI generates actionable recommendations
- **Live Scraping** — Real-time Instagram & LinkedIn data via RapidAPI
- **PDF Export** — Download full analytics report as PDF
- **4 Chart Types** — Bar, Line, Pie, and Radar charts

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS + Recharts |
| Backend | Python Flask + Flask-CORS |
| AI | Google Gemini API (gemini-1.5-flash) |
| Scraping | RapidAPI (Instagram + LinkedIn) |
| PDF | FPDF2 |

---

## 📁 Project Structure


---

## ⚙️ Setup & Run

### Backend
```bash
cd backend
pip install flask flask-cors google-genai fpdf2 requests
python app.py

###  Frontend
cd frontend
npm install
npm run dev
Open: http://localhost:5173

🔑 Environment Variables
Create a .env file in /backend:
GEMINI_API_KEY=your_gemini_key_here
RAPIDAPI_KEY=your_rapidapi_key_here

| Method | Endpoint                        | Description           |
| ------ | ------------------------------- | --------------------- |
| GET    | /api/profiles                   | All profiles          |
| GET    | /api/profiles/main              | Main profile          |
| GET    | /api/profiles/competitors       | Competitor profiles   |
| GET    | /api/comparison                 | Comparison data       |
| GET    | /api/insights                   | Gemini AI insights    |
| GET    | /api/scrape/instagram/:username | Live Instagram scrape |
| POST   | /api/scrape/linkedin            | Live LinkedIn scrape  |
| GET    | /api/export/pdf                 | Download PDF report   |


🏗️ Architecture
React Frontend (Vite)
      ↓ HTTP Requests
Flask Backend (Python)
      ↓              ↓
RapidAPI          Gemini AI
(Live Scraping)   (Insights)
      ↓
Mock Data Fallback

