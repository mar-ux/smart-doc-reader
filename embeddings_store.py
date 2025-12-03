# embeddings_store.py
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = "embeddings"
os.makedirs(INDEX_DIR, exist_ok=True)

INDEX_FILE = f"{INDEX_DIR}/faiss.index"
META_FILE = f"{INDEX_DIR}/meta.pkl"

class EmbeddingsStore:
    def __init__(self, model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(META_FILE, "rb") as f:
                self.meta = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def add(self, doc_id, text, filename):
        emb = self.model.encode([text]).astype("float32")
        self.index.add(emb)
        self.meta.append({"doc_id": doc_id, "filename": filename, "preview": text[:500]})
        self.save()

    def save(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(META_FILE, "wb") as f:
            pickle.dump(self.meta, f)

    def search(self, query, k=5):
        emb = self.model.encode([query]).astype("float32")
        D, I = self.index.search(emb, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < len(self.meta):
                results.append({"distance": float(score), "meta": self.meta[idx]})
        return results
