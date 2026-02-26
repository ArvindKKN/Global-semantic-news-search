import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import json

from backend.db import get_connection
from backend.services.embedding_service import generate_embedding
from backend.services.sentiment_service import analyze_sentiment

# Explicitly load backend/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("NEWS_API_KEY")

TOPICS = [

    "world",
    "global news",
    "international news",
    "breaking news",

    "technology",
    "business",
    "economy",
    "finance",
    "politics",
    "science",
    "health",
    "entertainment",

    "india",
    "china",
    "united states",
    "europe",
    "asia",
    "middle east",
    "africa",

    "artificial intelligence",
    "semiconductors",
    "electric vehicles",
    "startups",
    "cybersecurity"
]



def fetch_latest_news():

    conn = get_connection()
    cursor = conn.cursor()

    total_saved = 0

    for topic in TOPICS:

        url = (
            "https://newsapi.org/v2/everything?"
            f"q={topic}&"
            "language=en&"
            "sortBy=publishedAt&"
            "pageSize=20&"
            f"apiKey={API_KEY}"
        )

        response = requests.get(url)

        if response.status_code != 200:
            continue

        articles = response.json().get("articles", [])

        for article in articles:

            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "")
            url = article.get("url", "")

            if not title or not url:
                continue

            text = f"{title} {description}"

            sentiment = analyze_sentiment(text)
            embedding = generate_embedding(text)

            cursor.execute("""
                INSERT OR IGNORE INTO news
                (title, source, url, sentiment, published_at, embedding)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                title,
                source,
                url,
                sentiment,
                datetime.utcnow().isoformat(),
                json.dumps(embedding)
            ))

            total_saved += 1

    conn.commit()
    conn.close()

    return {
        "count": total_saved,
        "message": f"{total_saved} global articles fetched and indexed"
    }

def fetch_news_by_query(query):

    conn = get_connection()
    cursor = conn.cursor()

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={query}&"
        "language=en&"
        "sortBy=publishedAt&"
        "pageSize=20&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        conn.close()
        return []

    articles = response.json().get("articles", [])
    results = []

    for article in articles:

        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")
        url = article.get("url", "")

        if not title or not url:
            continue

        text = f"{title} {description}"

        sentiment = analyze_sentiment(text)
        embedding = generate_embedding(text)

        cursor.execute("""
            INSERT OR IGNORE INTO news
            (title, source, url, sentiment, published_at, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            source,
            url,
            sentiment,
            datetime.utcnow().isoformat(),
            json.dumps(embedding)
        ))

        results.append({
            "title": title,
            "source": source,
            "url": url
        })

    conn.commit()
    conn.close()

    return results













