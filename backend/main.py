from fastapi import FastAPI, Query
from .services.news_service import fetch_latest_news
from backend.db import init_db

app = FastAPI()
init_db()

@app.get("/")
def root():
    return {"message": "News Intelligence API Running ✅"}

@app.get("/news/latest")
def get_latest_news(
    category: str = Query("general", description="News category"),
    country: str = Query("us", description="Country code (us, in, gb, etc.)")
):
     return fetch_latest_news(country=country, category=category)
    


