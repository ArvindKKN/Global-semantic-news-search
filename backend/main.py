from fastapi import FastAPI
from backend.services.news_service import fetch_latest_news
from backend.services.retrieval_service import search_news
from backend.db import init_db, get_connection

app = FastAPI()

# Initialize DB on startup
init_db()


@app.get("/")
def root():
    return {"message": "Global Semantic News Search API Running ✅"}


# Global ingestion endpoint
@app.get("/news/latest")
def get_latest_news():
    return fetch_latest_news()


# Semantic search endpoint
@app.get("/news/search")
def search(q: str):
    return search_news(q)


# Optional: View stored articles
@app.get("/news/all")
def get_all_news():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title, source, url FROM news LIMIT 50")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"title": r[0], "source": r[1], "url": r[2]}
        for r in rows
    ]
















    




