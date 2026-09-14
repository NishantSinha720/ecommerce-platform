import os
from pathlib import Path
import numpy as np

INDEX_DIR = Path(__file__).resolve().parent / "vectorstore"
INDEX_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = INDEX_DIR / "catalog.npy"

def _docs():
    from products.models import Product
    return [
        {
            "id": p.id,
            "text": f"{p.name}. SKU {p.sku}. Price {p.price}. {p.description}",
        }
        for p in Product.objects.filter(is_active=True)
    ]

def _vector(text, size=256):
    # Deterministic lightweight embedding fallback.
    v = np.zeros(size, dtype=np.float32)
    for i, token in enumerate(text.lower().split()):
        v[hash(token) % size] += 1.0 / (i + 1)
    norm = np.linalg.norm(v)
    return v / norm if norm else v

def build_index():
    docs = _docs()
    vectors = np.vstack([_vector(x["text"]) for x in docs]) if docs else np.zeros((0, 256), dtype=np.float32)
    np.save(INDEX_FILE, vectors)
    return {"documents": len(docs), "dimension": 256}

def search(query, top_k=5):
    docs = _docs()
    if not docs:
        return []
    vectors = np.vstack([_vector(x["text"]) for x in docs])
    q = _vector(query)
    scores = vectors @ q
    order = np.argsort(-scores)[:top_k]
    return [
        {"id": docs[i]["id"], "text": docs[i]["text"], "score": round(float(scores[i]), 4)}
        for i in order
    ]
