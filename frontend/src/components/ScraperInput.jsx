import { useState } from 'react';

const ScraperInput = ({ onResult }) => {
  const [platform, setPlatform] = useState('instagram');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleScrape = async () => {
    if (!input.trim()) {
      setError('Please enter a username or URL');
      return;
    }
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      let res;

      if (platform === 'instagram') {
        res = await fetch(
          `/api/scrape/instagram/${input.trim()}`
       );
      } else {
        res = await fetch('/api/scrape/linkedin',  {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: input.trim() })
        });
      }

      const data = await res.json();

      if (data.error) {
        setError(`${data.error}`);
      } else {
        setSuccess(
          `Scraped @${data.username} — ${data.followers?.toLocaleString()} followers`
        );
        onResult(data);
        setInput('');
      }

    } catch {
      setError('Connection failed — make sure backend is running on port 5000');
    }

    setLoading(false);
  };

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-blue-100">

      {/* Title */}
      <div className="mb-3">
        <h3 className="font-bold text-gray-700 text-base">
          🔍 Scrape Live Profile
        </h3>
        <p className="text-gray-400 text-xs mt-1">
          Fetch real-time data from Instagram or LinkedIn via RapidAPI
        </p>
      </div>

      {/* Input Row */}
      <div className="flex gap-2 flex-wrap items-center">

        {/* Platform Dropdown */}
        <select
          value={platform}
          onChange={e => {
            setPlatform(e.target.value);
            setInput('');
            setError('');
            setSuccess('');
          }}
          className="border border-gray-200 rounded-lg px-3 py-2
            text-sm text-gray-600 bg-gray-50
            focus:outline-none focus:ring-2 focus:ring-blue-300">
          <option value="instagram">📷 Instagram</option>
          <option value="linkedin">💼 LinkedIn</option>
        </select>

        {/* Text Input */}
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleScrape()}
          placeholder={
            platform === 'instagram'
              ? 'Enter username — e.g. natgeo'
              : 'Enter LinkedIn URL — e.g. linkedin.com/in/satyanadella'
          }
          className="flex-1 border border-gray-200 rounded-lg px-3 py-2
            text-sm bg-gray-50 min-w-48
            focus:outline-none focus:ring-2 focus:ring-blue-300"
        />

        {/* Scrape Button */}
        <button
          onClick={handleScrape}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700
            disabled:bg-gray-300 disabled:cursor-not-allowed
            text-white px-5 py-2 rounded-lg text-sm
            font-medium transition-all">
          {loading ? '⏳ Scraping...' : '🚀 Scrape'}
        </button>

      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-3 bg-red-50 border border-red-200
          rounded-lg px-4 py-2">
          <p className="text-red-600 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="mt-3 bg-green-50 border border-green-200
          rounded-lg px-4 py-2">
          <p className="text-green-600 text-sm font-medium">
            ✅ {success}
          </p>
        </div>
      )}

      {/* Footer Note */}
      <p className="text-gray-300 text-xs mt-3">
        * Uses RapidAPI for live data — falls back to mock data if API unavailable
      </p>

    </div>
  );
};

export default ScraperInput;
