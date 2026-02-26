import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Global Semantic News Search Engine", layout="wide")

st.title("🌍 Global Semantic News Search Engine")
st.caption("Search latest global news by topic, person, company, or event")
st.divider()

# Fetch latest news

st.subheader("🔄 Fetch Latest Global News")

if st.button("Fetch Latest News"):

    try:

        res = requests.get(f"{API_BASE}/news/latest")

        if res.status_code == 200:

            data = res.json()
            st.success(data["message"])

        else:
            st.error("Failed to fetch news")

    except:
        st.error("Backend not running")
st.divider()        


# Semantic search

st.subheader("🔎 Search Global News")

query = st.text_input(
    "Enter topic, person, company, or event:",
    placeholder="e.g., Rajinikanth, AI startup, Events..."
)

col1, col2 = st.columns([1, 4])

with col1:
    search_clicked = st.button("Search")

if search_clicked:

    if not query.strip():
        st.warning("Please enter a search term.")
    else:
        with st.spinner("Searching indexed articles..."):

            try:
                res = requests.get(f"{API_BASE}/news/search", params={"q": query})
                results = res.json()

                if results:

                    st.success(f"Found {len(results)} relevant articles")

                    for article in results:
                        with st.container():
                            st.markdown(f"### {article['title']}")
                            st.caption(f"Source: {article['source']}")
                            st.markdown(f"[Read Full Article]({article['url']})")
                            st.divider()

                else:
                    st.info("No relevant articles found in indexed dataset.")

            except:
                st.error("Backend not running or connection failed.")
st.divider()                  
                

# -------------------------
# Refresh Section
# -------------------------
st.subheader("🔄 Update News Index")

if st.button("Fetch Latest News (Global Seed)"):
    with st.spinner("Fetching and indexing global news..."):
        try:
            res = requests.get(f"{API_BASE}/news/latest")
            data = res.json()
            st.success(data.get("message", "News fetched"))
        except:
            st.error("Backend not running.")








