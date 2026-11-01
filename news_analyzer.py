import streamlit as st
import feedparser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# NLTK VADER lexicon download (App ke liye zaroori)
nltk.download('vader_lexicon', quiet=True)

# Page ki setting
st.set_page_config(page_title="Veer Market Scanner", page_icon="🌍", layout="wide")

st.title("🌍 VEER MASTER: World Market News & Sector Impact")
st.write("Live sentiment analysis for global economy & stock markets.")

# 🔴 NAYA FEATURE: Refresh aur WhatsApp Share Button ek sath
col1, col2 = st.columns([1, 4])

with col1:
    if st.button("🔄 Refresh Live News Now"):
        st.cache_data.clear()

with col2:
    # WhatsApp Share Link
    whatsapp_text = "Hello! Maine ek Live Global Market News aur Sector Impact Scanner banaya hai. Aap ise yahan check kar sakte hain: https://veer-market-news.streamlit.app/"
    st.link_button("📲 Share on WhatsApp", f"https://wa.me/?text={whatsapp_text}")

st.divider()

# News fetch karne ka function
@st.cache_data(ttl=60)
def fetch_market_news():
    rss_url = "https://news.google.com/rss/search?q=global+economy+stock+market+when:1d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    for entry in feed.entries[:15]:
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if hasattr(entry, 'published') else "Time not available"
        })
    return news_list

def analyze_sector_impact(news_list):
    sia = SentimentIntensityAnalyzer()
    
    sector_keywords = {
        "Technology / IT": ["tech", "apple", "amd", "ai", "software", "semiconductor", "palantir", "cyber"],
        "Banking & Finance": ["bank", "rates", "inflation", "tax", "fed", "economy", "pension", "rbi", "interest"],
        "Energy & Commodities": ["oil", "gas", "energy", "steel", "gold", "mineral", "mining", "crude"],
        "Healthcare & Pharma": ["health", "pharma", "vaccine", "moderna", "hospital", "fda"],
        "Automobile / EV": ["auto", "ev", "byd", "tesla", "vehicles", "motors"],
        "Real Estate & Housing": ["housing", "real estate", "property", "mortgage"],
        "FMCG / Retail": ["retail", "consumer", "garment", "fmcg", "sales", "store"]
    }
    
    for news in news_list:
        headline = news["title"]
        sentiment_score = sia.polarity_scores(headline)
        compound = sentiment_score['compound']
        
        if compound >= 0.05:
            sentiment = "🟢 POSITIVE"
        elif compound <= -0.05:
            sentiment = "🔴 NEGATIVE"
        else:
            sentiment = "⚪ NEUTRAL"
            
        impacted_sectors = []
        headline_lower = headline.lower()
        for sector, keywords in sector_keywords.items():
            if any(word in headline_lower for word in keywords):
                impacted_sectors.append(sector)
        
        if not impacted_sectors:
            impacted_sectors = ["Broad Market / Macro Economy"]
            
        # Streamlit Expander ka use
        with st.expander(f"{sentiment} | {headline}"):
            st.write(f"**🏢 Impact Sector:** {', '.join(impacted_sectors)}")
            st.write(f"**🕒 Time:** {news['published']}")
            st.markdown(f"**[🔗 Poori News Padhne Ke Liye Yahan Click Karein]({news['link']})**")

# Script run karna
with st.spinner("Fetching Live News..."):
    news_data = fetch_market_news()
    if news_data:
        analyze_sector_impact(news_data)
    else:
        st.error("News fetch nahi ho payi, thodi der baad try karein.")
