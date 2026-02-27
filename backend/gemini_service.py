from google import genai

client = genai.Client(api_key="AIzaSyC3K6g5V7dSDKEQTlU3YthMeQ0yRH3sMmU")

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
    competitor_summary = ""
    for c in competitors:
        competitor_summary += f"""
        - {c['username']}: {c['followers']} followers,
          {c['engagement_rate']}% engagement,
          top content: {c['top_content_type']}
        """

    prompt = f"""
    You are a social media growth expert for an EdTech company in India.

    Analyze this Instagram profile and compare with competitors:

    MAIN PROFILE: {main_profile['username']}
    - Followers: {main_profile['followers']}
    - Engagement Rate: {main_profile['engagement_rate']}%
    - Top Content Type: {main_profile['top_content_type']}
    - Posting Frequency: {main_profile['posting_frequency']} posts/day
    - Best Posting Time: {main_profile['best_posting_time']}

    COMPETITORS:
    {competitor_summary}

    Give exactly this structure:
    STRENGTHS:
    - (2 specific strengths)

    COMPETITORS DOING BETTER:
    - (2 specific points)

    CONTENT GAPS:
    - (2 specific suggestions)

    BEST TIME TO POST:
    - (specific recommendation)

    CONTENT RECOMMENDATION:
    - (specific recommendation)

    GROWTH STRATEGY:
    - (1 overall strategy)

    Be specific, actionable, and relevant to EdTech/Commerce education niche.
    """

    try:
        # Try models in order until one works
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.0-pro"
        ]
        
        response_text = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                response_text = response.text
                break
            except Exception:
                continue
        
        if response_text:
            return response_text
        else:
            return get_fallback_insights(main_profile, competitors)
            
    except Exception as e:
        return get_fallback_insights(main_profile, competitors)

