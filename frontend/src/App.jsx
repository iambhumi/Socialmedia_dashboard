import { useState, useEffect } from 'react';
import ProfileCard from './components/ProfileCard';
import AIInsights from './components/AIInsights';
import ScraperInput from './components/ScraperInput';
import {
  FollowerBarChart,
  EngagementBarChart,
  GrowthLineChart,
  ContentPieChart,
  CompetitorRadarChart
} from './components/Charts';

const API = 'http://localhost:5000/api';

export default function App() {

  const [profiles, setProfiles]               = useState([]);
  const [mainProfile, setMainProfile]         = useState(null);
  const [comparison, setComparison]           = useState([]);
  const [insights, setInsights]               = useState('');
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [activeTab, setActiveTab]             = useState('overview');
  const [scrapedProfiles, setScrapedProfiles] = useState([]);
  const [liveCompetitors, setLiveCompetitors] = useState([]);
  const [isLiveMode, setIsLiveMode]           = useState(false);

  // ── Load mock data on start ───────────────────────────────
  useEffect(() => {
    fetch(`${API}/profiles`).then(r => r.json()).then(setProfiles);
    fetch(`${API}/comparison`).then(r => r.json()).then(setComparison);
    if (!isLiveMode) {
    fetch(`${API}/profiles/main`).then(r => r.json()).then(setMainProfile);
  }
  }, []);

  // ── When a profile is scraped ─────────────────────────────
  const handleScrapeResult = (data) => {

    // avoid duplicates in scraped list
    setScrapedProfiles(prev => {
      const exists = prev.find(p => p.username === data.username);
      if (exists) return prev;
      return [...prev, data];
    });

    if (!isLiveMode) {
      // ── FIRST scrape → becomes main profile ──────────────
      data.type = 'main';
      setMainProfile(data);
      setIsLiveMode(true);
      setLiveCompetitors([]);
      setComparison([{
        username:         data.username,
        followers:        data.followers,
        engagement_rate:  data.engagement_rate,
        avg_likes:        data.avg_likes,
        posting_frequency: data.posting_frequency
      }]);

    } else {
      // ── SUBSEQUENT scrapes → become competitors ───────────
      data.type = 'competitor';
      setLiveCompetitors(prev => {
        const exists = prev.find(p => p.username === data.username);
        if (exists) return prev;
        const updated = [...prev, data];

        // rebuild comparison with main + all competitors
        setComparison([
          {
            username:          mainProfile.username,
            followers:         mainProfile.followers,
            engagement_rate:   mainProfile.engagement_rate,
            avg_likes:         mainProfile.avg_likes,
            posting_frequency: mainProfile.posting_frequency
          },
          ...updated.map(c => ({
            username:          c.username,
            followers:         c.followers,
            engagement_rate:   c.engagement_rate,
            avg_likes:         c.avg_likes,
            posting_frequency: c.posting_frequency
          }))
        ]);
        return updated;
      });
    }
    setInsights(''); // reset insights on every new scrape
  };

  // ── competitors: live if scraped, mock otherwise ──────────
  const competitors = isLiveMode
    ? liveCompetitors
    : profiles.filter(p => p.type === 'competitor');

  // ── Gemini Insights — POST with real data ─────────────────
  const fetchInsights = async () => {
    if (!mainProfile) return;
    setInsightsLoading(true);
    setActiveTab('insights');
    try {
      const res = await fetch(`${API}/insights`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_profile:        mainProfile,
          competitor_profiles: competitors
        })
      });
      const data = await res.json();
      setInsights(data.insights || 'No insights returned.');
    } catch {
      setInsights(' Error fetching insights.');
    }
    setInsightsLoading(false);
  };

  const exportPDF = async () => {
  try {
    const allProfiles = mainProfile ? [mainProfile, ...competitors] : [];

    const res = await fetch(`${API}/export/pdf`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profiles: allProfiles,
        insights: insights || ''
      })
    });

    if (!res.ok) {
      const err = await res.json();
      alert('PDF error: ' + err.error);
      return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ArivuPro_Analytics_Report.pdf';
    a.click();
    window.URL.revokeObjectURL(url);

  } catch (e) {
    alert('Failed to export PDF');
    console.error(e);
  }
};

  const tabs = ['overview', 'competitors', 'charts', 'insights'];

  return (
    <div className="min-h-screen bg-gray-50">

      {/* ── Header ─────────────────────────────────────── */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 shadow-lg">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">📊 Social Media Analytics Dashboard</h1>
            <p className="text-blue-100 mt-1 text-sm">
              Track performance & competitor intelligence — Powered by Gemini AI
            </p>
          </div>
          <button onClick={exportPDF}
            className="bg-white text-blue-600 font-semibold px-4 py-2 rounded-lg text-sm hover:bg-blue-50 transition-all shadow-sm">
            📄 Export PDF
          </button>
        </div>
      </div>

      {/* ── Tab Bar ────────────────────────────────────── */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="flex max-w-6xl mx-auto">
          {tabs.map(tab => (
            <button key={tab}
              onClick={() => tab === 'insights' ? fetchInsights() : setActiveTab(tab)}
              className={`px-6 py-4 font-medium capitalize transition-all text-sm
                ${activeTab === tab
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'}`}>
              {tab === 'overview'     && '🏠 Overview'}
              {tab === 'competitors'  && '⚔️ Competitors'}
              {tab === 'charts'       && '📈 Charts'}
              {tab === 'insights'     && '🤖 AI Insights'}
            </button>
          ))}
        </div>
      </div>

      {/* ── Page Body ──────────────────────────────────── */}
      <div className="max-w-6xl mx-auto p-6">

        {/* Scraper always visible */}
        <ScraperInput onResult={handleScrapeResult} />

        {/* Live mode badge */}
        {mainProfile && (
          <p className="text-center text-xs mt-2 text-gray-400">
            {isLiveMode
              ? liveCompetitors.length > 0
                ? ` Live — @${mainProfile.username} + ${liveCompetitors.length} competitor(s) | scrape more to add`
                : ` Live — @${mainProfile.username} is main | scrape another profile to add a competitor`
              : ' Demo data — scrape a profile to switch to live mode'}
          </p>
        )}

        

        <div className="my-6 border-t border-gray-200" />

        {/* ══ OVERVIEW*/}
        {activeTab === 'overview' && mainProfile && (
          <div>
            {/* Scraped profiles row */}
        {scrapedProfiles.length > 0 && (
          <div className="mt-6">
            <h3 className="font-bold text-gray-600 mb-3 flex items-center gap-2">
              📡 Live Scraped Profiles
              <span className="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full">
                {scrapedProfiles.length} fetched
              </span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {scrapedProfiles.map(p => (
                <ProfileCard key={p.username} profile={p} isMain={false} />
              ))}
            </div>
          </div>
        )}
            <h2 className="text-xl font-bold mb-4 text-gray-700">Your Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <ProfileCard profile={mainProfile} isMain={true} />
              <div className="bg-white p-4 rounded-xl shadow-sm">
                <h3 className="font-semibold text-gray-600 mb-3">📈 Follower Growth Trend</h3>
                <GrowthLineChart data={mainProfile.follower_growth || []} />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-xl shadow-sm">
                <h3 className="font-semibold text-gray-600 mb-3">🎬 Content Type Distribution</h3>
                <ContentPieChart data={mainProfile.content_types || {}} />
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm">
                <h3 className="font-semibold text-gray-600 mb-3">📊 Quick Stats</h3>
                <div className="space-y-3 mt-2">
                  {[
                    { label: 'Average Likes',    value: mainProfile.avg_likes,    color: 'blue'   },
                    { label: 'Average Comments', value: mainProfile.avg_comments, color: 'green'  },
                    { label: 'Average Shares',   value: mainProfile.avg_shares,   color: 'purple' },
                    { label: 'Total Posts',      value: mainProfile.total_posts,  color: 'orange' },
                    { label: 'Following',        value: mainProfile.following,    color: 'pink'   },
                  ].map(stat => (
                    <div key={stat.label}
                      className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600 text-sm">{stat.label}</span>
                      <span className={`font-bold text-${stat.color}-600`}>
                        {stat.value?.toLocaleString() ?? '—'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ══ COMPETITORS  */}
        {activeTab === 'competitors' && (
          <div>
            <h2 className="text-xl font-bold mb-4 text-gray-700">
              Competitor Profiles
              {isLiveMode && liveCompetitors.length === 0 && (
                <span className="text-sm font-normal text-gray-400 ml-2">
                  — scrape a 2nd profile to add one
                </span>
              )}
            </h2>
            {competitors.length === 0
              ? <p className="text-gray-400 text-sm">No competitors loaded yet.</p>
              : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {competitors.map(p => (
                    <ProfileCard key={p.username} profile={p} isMain={false} />
                  ))}
                </div>
              )
            }
          </div>
        )}

        {/* ══ CHARTS  */}
        {activeTab === 'charts' && (
          <div className="space-y-6">
            {comparison.length === 0
              ? <p className="text-gray-400 text-sm">No chart data yet — scrape a profile first.</p>
              : <>
                <div className="bg-white p-6 rounded-xl shadow-sm">
                  <h3 className="font-semibold text-gray-700 mb-4">👥 Follower Count Comparison</h3>
                  <FollowerBarChart data={comparison} />
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm">
                  <h3 className="font-semibold text-gray-700 mb-4">💫 Engagement Rate vs Posting Frequency</h3>
                  <EngagementBarChart data={comparison} />
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm">
                  <h3 className="font-semibold text-gray-700 mb-4">🎯 Multi-Metric Radar</h3>
                  <CompetitorRadarChart data={comparison} />
                </div>
              </>
            }
          </div>
        )}

        {/* ══ AI INSIGHTS  */}
        {activeTab === 'insights' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-700">🤖 Gemini AI Insights</h2>
              <button onClick={fetchInsights}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition-all">
                 Refresh Insights
              </button>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-xl">
              <AIInsights insights={insights} loading={insightsLoading} />
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
