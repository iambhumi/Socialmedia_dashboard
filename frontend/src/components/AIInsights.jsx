const AIInsights = ({ insights, loading }) => {
  if (loading) return (
    <div className="flex items-center justify-center h-40">
      <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
      <p className="ml-3 text-gray-500">Generating AI Insights...</p>
    </div>
  );

  if (!insights) return null;

  // Parse insights into sections
  const sections = insights.split('\n\n').filter(s => s.trim());

  return (
    <div className="space-y-3">
      {sections.map((section, index) => {
        const lines = section.split('\n').filter(l => l.trim());
        const title = lines[0];
        const points = lines.slice(1);

        return (
          <div key={index} className="bg-white rounded-lg p-4 shadow-sm border-l-4 border-blue-400">
            <h4 className="font-semibold text-blue-700 mb-2">{title}</h4>
            {points.map((point, i) => (
              <p key={i} className="text-gray-600 text-sm ml-2">{point}</p>
            ))}
          </div>
        );
      })}
    </div>
  );
};

export default AIInsights;
