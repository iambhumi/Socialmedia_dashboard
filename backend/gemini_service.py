from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def get_fallback_insights(main_profile, competitors):
    # Find best competitor
    best = max(competitors, key=lambda x: x['engagement_rate'])
    avg_engagement = sum(c['engagement_rate'] for c in competitors) / len(competitors)
    
    return f"""STRENGTHS:
- Strong follower base of {main_profile['followers']:,} with consistent {main_profile['engagement_rate']}% engagement rate
- Top content type '{main_profile['top_content_type']}' aligns with current platform trends

COMPETITORS DOING BETTER:
- {best['username']} leads with {best['engagement_rate']}% engagement vs your {main_profile['engagement_rate']}%
- Competitors post {round(avg_engagement, 1)} avg posts/day vs your {main_profile['posting_frequency']} posts/day

CONTENT GAPS:
- Increase Reels production — competitors using Reels as primary content show higher engagement
- Add more carousel posts for educational content — high save rates in EdTech niche

BEST TIME TO POST:
- Your current best time {main_profile['best_posting_time']} is good — maintain consistency daily

CONTENT RECOMMENDATION:
- Focus on short-form Reels (15-30 seconds) with exam tips, quick tricks, and success stories

GROWTH STRATEGY:
- Collaborate with CA/CS toppers for testimonial content — social proof drives enrollment conversions in EdTech"""


def generate_insights(main_profile, competitors):
    platform = main_profile.get("platform", "instagram")
    username = main_profile.get("username", "User")
    niche = "social media"

    competitor_summary = ""
    for c in competitors:
        competitor_summary += f"\n- @{c['username']}: {c.get('followers',0):,} followers, {c.get('engagement_rate',0)}% engagement, top content: {c.get('top_content_type','N/A')}"

   
    prompt = f"""
You are a social media growth expert analyzing a {platform} profile.

MAIN PROFILE: @{username}
- Followers: {main_profile.get('followers', 0):,}
- Engagement Rate: {main_profile.get('engagement_rate', 0)}%
- Top Content Type: {main_profile.get('top_content_type', 'N/A')}
- Posting Frequency: {main_profile.get('posting_frequency', 0)} posts/day
- Best Posting Time: {main_profile.get('best_posting_time', 'N/A')}
- Platform: {platform}

COMPETITORS:
{competitor_summary if competitor_summary else "No competitors added yet."}

Give exactly this structure:
STRENGTHS:
- (2 specific strengths based on actual data)

COMPETITORS DOING BETTER:
- (2 specific points, or note if no competitors)

CONTENT GAPS:
- (2 actionable suggestions for {platform})

BEST TIME TO POST:
- (specific time recommendation for {platform})

CONTENT RECOMMENDATION:
- (specific content format recommendation)

GROWTH STRATEGY:
- (1 clear actionable strategy)

Be specific, data-driven, and platform-aware.
"""
    try:
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.0-pro"]
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                if response.text:
                    return response.text
            except Exception:
                continue
        return get_fallback_insights(main_profile, competitors)
    except Exception:
        return get_fallback_insights(main_profile, competitors)