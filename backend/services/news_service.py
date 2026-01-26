import requests
import os
from dotenv import load_dotenv
from textblob import TextBlob
from datetime import datetime

from backend.db import get_connection
import json
from backend.services.embedding_service import generate_embedding

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

API_KEY = os.getenv("NEWS_API_KEY")

def analyze_sentiment(text):
    """Simple sentiment using TextBlob polarity"""
    if not text:
        return "Neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"
    

def save_article(article):
    conn = get_connection()
    cursor = conn.cursor()
    
    text_for_embedding = article["title"]
    embedding = generate_embedding(text_for_embedding)
    
    try:
        cursor.execute("""   
            INSERT OR IGNORE INTO news
            (title, source, url, sentiment, published_at, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            article["title"],
            article["source"],
            article["url"],
            article["sentiment"],
            datetime.utcnow().isoformat(),
            json.dumps(embedding)
        ))
        conn.commit()
    except Exception as e:
        print("DB insert error:", e)
    finally:
        conn.close()


def fetch_latest_news(country="us", category="general"):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch news", "status": response.status_code}

    data = response.json()
    articles = data.get("articles", [])
    cleaned = []

    for article in articles:
        news_item = {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "sentiment": analyze_sentiment(article["title"])
        }

        save_article(news_item)        # 🔥 THIS NOW RUNS
        cleaned.append(news_item)      # ✅ correct list

    return {"count": len(cleaned), "articles": cleaned}










