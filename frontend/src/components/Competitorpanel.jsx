import { useState } from 'react';
import { scrapeCompetitor } from '../api';

export default function CompetitorPanel({ onCompetitorAdded }) {
  const [platform, setPlatform] = useState('instagram');
  const [identifier, setIdentifier] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAdd = async () => {
    if (!identifier.trim()) return;
    setLoading(true);
    setError('');
    try {
      const res = await scrapeCompetitor(platform, identifier.trim());
      if (res.success) {
        onCompetitorAdded(res.data);
        setIdentifier('');
      } else {
        setError(res.error || 'Failed to fetch competitor');
      }
    } catch {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div className="competitor-panel">
      <h3>Add Competitor</h3>
      <select value={platform} onChange={e => setPlatform(e.target.value)}>
        <option value="instagram">Instagram</option>
        <option value="linkedin">LinkedIn</option>
      </select>
      <input
        type="text"
        placeholder={platform === 'instagram' ? 'Enter username e.g. bbcnews' : 'Enter LinkedIn URL'}
        value={identifier}
        onChange={e => setIdentifier(e.target.value)}
      />
      <button onClick={handleAdd} disabled={loading}>
        {loading ? 'Fetching...' : '+ Add Competitor'}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
