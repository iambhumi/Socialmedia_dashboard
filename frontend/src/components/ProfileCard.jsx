const ProfileCard = ({ profile, isMain }) => {
  return (
    <div className={`p-4 rounded-xl shadow-md border-2 
      ${isMain ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white'}`}>
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold text-lg">@{profile.username}</h3>
        {isMain && (
          <span className="bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
            Your Profile
          </span>
        )}
      </div>
      <p className="text-gray-500 text-sm mb-3">{profile.bio}</p>
      <div className="grid grid-cols-2 gap-2">
        <div className="bg-white rounded-lg p-2 text-center shadow-sm">
          <p className="text-xl font-bold text-blue-600">
            {profile.followers.toLocaleString()}
          </p>
          <p className="text-xs text-gray-500">Followers</p>
        </div>
        <div className="bg-white rounded-lg p-2 text-center shadow-sm">
          <p className="text-xl font-bold text-green-600">
            {profile.engagement_rate}%
          </p>
          <p className="text-xs text-gray-500">Engagement</p>
        </div>
        <div className="bg-white rounded-lg p-2 text-center shadow-sm">
          <p className="text-xl font-bold text-purple-600">
            {profile.total_posts}
          </p>
          <p className="text-xs text-gray-500">Posts</p>
        </div>
        <div className="bg-white rounded-lg p-2 text-center shadow-sm">
          <p className="text-xl font-bold text-orange-600">
            {profile.posting_frequency}
          </p>
          <p className="text-xs text-gray-500">Posts/Day</p>
        </div>
      </div>
      <div className="mt-2 text-center">
        <span className="bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded-full">
          🏆 Top: {profile.top_content_type}
        </span>
        <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full ml-2">
          ⏰ {profile.best_posting_time}
        </span>
      </div>
    </div>
  );
};

export default ProfileCard;
