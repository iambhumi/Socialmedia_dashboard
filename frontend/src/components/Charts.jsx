import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, LineChart, Line, PieChart, Pie, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer
} from 'recharts';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

export const FollowerBarChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="username" tick={{ fontSize: 11 }} />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="followers" fill="#3B82F6" name="Followers" radius={[4,4,0,0]} />
    </BarChart>
  </ResponsiveContainer>
);

export const EngagementBarChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="username" tick={{ fontSize: 11 }} />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="engagement_rate" fill="#10B981" name="Engagement Rate %" radius={[4,4,0,0]} />
      <Bar dataKey="posting_frequency" fill="#F59E0B" name="Posts/Day" radius={[4,4,0,0]} />
    </BarChart>
  </ResponsiveContainer>
);

export const GrowthLineChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="month" tick={{ fontSize: 11 }} />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="followers" stroke="#3B82F6"
        strokeWidth={2} dot={{ fill: '#3B82F6' }} name="Followers" />
    </LineChart>
  </ResponsiveContainer>
);

export const ContentPieChart = ({ data }) => {
  const pieData = Object.entries(data).map(([name, value]) => ({ name, value }));
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={pieData} cx="50%" cy="50%" outerRadius={100}
          dataKey="value" label={({ name, value }) => `${name}: ${value}%`}>
          {pieData.map((entry, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
};

export const CompetitorRadarChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <RadarChart data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="username" tick={{ fontSize: 11 }} />
      <Radar name="Engagement" dataKey="engagement_rate"
        stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
      <Legend />
      <Tooltip />
    </RadarChart>
  </ResponsiveContainer>
);
