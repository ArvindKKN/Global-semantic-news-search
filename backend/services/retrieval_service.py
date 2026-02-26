import numpy as np
import json
from backend.db import get_connection
from backend.services.embedding_service import generate_embedding
from backend.services.news_service import fetch_news_by_query

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def search_news(query: str, top_k: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    # generate query embedding
    query_embedding = generate_embedding(query)

    cursor.execute("SELECT title, source, url, embedding FROM news WHERE embedding IS NOT NULL")
    rows = cursor.fetchall()

    scored = []

    for title, source, url, emb in rows:
        article_embedding = json.loads(emb)

        score = cosine_similarity(query_embedding, article_embedding)

        scored.append((score, {
            "title": title,
            "source": source,
            "url": url
        }))

    conn.close()

    # sort by highest similarity
    scored.sort(reverse=True, key=lambda x: x[0])

    # get top results
    top_results = scored[:top_k]

    # if no data in DB at all
    #if not top_results:
        #fetch_news_by_query(query)
        #return search_news(query)

    # check similarity threshold
    best_score = top_results[0][0]

    # If similarity too low, trigger fallback
    #if best_score < 0.35:   # threshold can be tuned
        #fetch_news_by_query(query)
        #return search_news(query)

    # otherwise return results
    return [item[1] for item in top_results]











