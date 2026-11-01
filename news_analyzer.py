import streamlit as st
import feedparser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# NLTK data download
nltk.download('vader_lexicon', quiet=True)

# Page Configuration
st.set_page_config(page_title="World Market News Scanner", layout="wide")
st.title("🌍 World Market News & Sector Impact Analysis")
st.markdown("Live sentiment tracking for global markets.")

@st.cache_data(ttl=600) # 10 minute tak data cache karega taaki fast load ho
def fetch_and_analyze_news():
    rss_url = "https://news.google.com/rss/search?q=global+economy+stock+market&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    sia = SentimentIntensityAnalyzer()
    
    sector_keywords = {
        "Technology / IT": ["tech", "apple", "amd", "ai", "software", "semiconductor", "palantir", "cyber"],
        "Banking & Finance": ["bank", "rates", "inflation", "tax", "fed", "economy", "pension", "rbi", "interest"],
        "Energy & Commodities": ["oil", "gas", "energy", "steel", "gold", "mineral", "mining", "crude"],
        "Healthcare & Pharma": ["health", "pharma", "vaccine", "moderna", "hospital", "fda"],
        "Automobile / EV": ["auto", "ev", "byd", "tesla", "vehicles", "motors"],
        "Real Estate": ["housing", "real estate", "property", "mortgage"],
        "FMCG / Retail": ["retail", "consumer", "garment", "fmcg", "sales", "store"]
    }
    
    results = []
    
    for entry in feed.entries[:20]:
        headline = entry.title
        score = sia.polarity_scores(headline)['compound']
        
        if score >= 0.05:
            sentiment = "🟢 POSITIVE"
        elif score <= -0.05:
            sentiment = "🔴 NEGATIVE"
        else:
            sentiment = "⚪ NEUTRAL"
            
        impacted_sectors = [sec for sec, keys in sector_keywords.items() if any(k in headline.lower() for k in keys)]
        sector_str = ", ".join(impacted_sectors) if impacted_sectors else "Macro Economy"
        
        results.append({
            "News Headline": headline,
            "Sentiment": sentiment,
            "Impacted Sector": sector_str
        })
        
    return pd.DataFrame(results)

# Fetch Data and Display in App
if st.button("🔄 Refresh Live News"):
    st.cache_data.clear()

df = fetch_and_analyze_news()

# Table format mein show karna
st.dataframe(df, use_container_width=True, hide_index=True)
