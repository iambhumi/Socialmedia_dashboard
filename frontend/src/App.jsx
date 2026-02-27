import { useState, useEffect } from 'react';
import ProfileCard from './components/Profilecard';
import AIInsights from './components/AIInsights';
import {
  FollowerBarChart, EngagementBarChart,
  GrowthLineChart, ContentPieChart, CompetitorRadarChart
} from './components/Charts';

const API = 'http://localhost:5000/api';

export default function App() {
  const [profiles, setProfiles] = useState([]);
  const [mainProfile, setMainProfile] = useState(null);
  const [comparison, setComparison] = useState([]);
  const [insights, setInsights] = useState('');
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  
  const exportPDF = () => {
  window.open('http://localhost:5000/api/export/pdf', '_blank');
};


  useEffect(() => {
    fetch(`${API}/profiles`).then(r => r.json()).then(setProfiles);
    fetch(`${API}/profiles/main`).then(r => r.json()).then(setMainProfile);
    fetch(`${API}/comparison`).then(r => r.json()).then(setComparison);
  }, []);

  const fetchInsights = async () => {
    setInsightsLoading(true);
    setActiveTab('insights');
    const res = await fetch(`${API}/insights`);
    const data = await res.json();
    setInsights(data.insights);
    setInsightsLoading(false);
  };

  const competitors = profiles.filter(p => p.type === 'competitor');

  const tabs = ['overview', 'competitors', 'charts', 'insights'];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 shadow-lg">
        <h1 className="text-3xl font-bold">📊 Social Media Analytics Dashboard</h1>
        <p className="text-blue-100 mt-1">Track performance & competitor intelligence</p>
        <button
  onClick={exportPDF}
  className="mt-3 bg-white text-blue-600 font-semibold
    px-4 py-2 rounded-lg text-sm hover:bg-blue-50 transition-all">
  📄 Export PDF Report
</button>

      </div>

      {/* Tabs */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="flex max-w-6xl mx-auto">
          {tabs.map(tab => (
            <button key={tab}
              onClick={() => tab === 'insights' ? fetchInsights() : setActiveTab(tab)}
              className={`px-6 py-4 font-medium capitalize transition-all
                ${activeTab === tab
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'}`}>
              {tab === 'insights' ? '🤖 AI Insights' : tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">

        {/* Overview Tab */}
        {activeTab === 'overview' && mainProfile && (
          <div>
            <h2 className="text-xl font-bold mb-4 text-gray-700">Your Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <ProfileCard profile={mainProfile} isMain={true} />
              <div>
                <h3 className="font-semibold text-gray-600 mb-3">📈 Follower Growth Trend</h3>
                <div className="bg-white p-4 rounded-xl shadow-sm">
                  <GrowthLineChart data={mainProfile.follower_growth} />
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-xl shadow-sm">
                <h3 className="font-semibold text-gray-600 mb-3">🎬 Content Type Distribution</h3>
                <ContentPieChart data={mainProfile.content_types} />
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm">
                <h3 className="font-semibold text-gray-600 mb-3">📊 Quick Stats</h3>
                <div className="space-y-3 mt-4">
                  {[
                    { label: 'Average Likes', value: mainProfile.avg_likes, color: 'blue' },
                    { label: 'Average Comments', value: mainProfile.avg_comments, color: 'green' },
                    { label: 'Average Shares', value: mainProfile.avg_shares, color: 'purple' },
                    { label: 'Total Posts', value: mainProfile.total_posts, color: 'orange' },
                  ].map(stat => (
                    <div key={stat.label} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">{stat.label}</span>
                      <span className={`font-bold text-${stat.color}-600`}>{stat.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Competitors Tab */}
        {activeTab === 'competitors' && (
          <div>
            <h2 className="text-xl font-bold mb-4 text-gray-700">Competitor Profiles</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-4">
              {competitors.map(profile => (
                <ProfileCard key={profile.username} profile={profile} isMain={false} />
              ))}
            </div>
          </div>
        )}

        {/* Charts Tab */}
        {activeTab === 'charts' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="font-semibold text-gray-700 mb-4">👥 Follower Count Comparison</h3>
              <FollowerBarChart data={comparison} />
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="font-semibold text-gray-700 mb-4">💫 Engagement Rate & Posting Frequency</h3>
              <EngagementBarChart data={comparison} />
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="font-semibold text-gray-700 mb-4">🎯 Multi-Metric Radar Comparison</h3>
              <CompetitorRadarChart data={comparison} />
            </div>
          </div>
        )}

        {/* AI Insights Tab */}
        {activeTab === 'insights' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-700">🤖 Gemini AI Insights</h2>
              <button onClick={fetchInsights}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition-all">
                🔄 Refresh Insights
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
