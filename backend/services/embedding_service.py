from sentence_transformers import SentenceTransformer

# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    if not text:
        return None
    embedding = model.encode(text)
    return embedding.tolist()


