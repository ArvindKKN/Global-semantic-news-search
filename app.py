import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="News Intelligence Dashboard", layout="wide")
st.title("📰 News Intelligence Dashboard(AI-Powered)")
st.subheader("Analyze live news sentiment in real time")

# --- Filters ---
country = st.selectbox("🌍 Select Country", ["us", "in", "gb", "au", "ca"])
category = st.selectbox("🗂️ Select Category", ["general", "business", "technology", "sports", "science", "entertainment", "health"])

if st.button("Fetch News"):
    API_URL = f"http://127.0.0.1:8000/news/latest?country={country}&category={category}"
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        if len(articles) == 0:
            st.warning("😕 No news articles found for this selection. Try another category or country.")
        else:
            df = pd.DataFrame(articles)
            st.success(f"✅ Showing {len(df)} articles for {category.capitalize()} ({country.upper()})")
            st.dataframe(df)
    else:
        st.error("Failed to fetch news from backend")

        



    

    