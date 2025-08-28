import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

# ------------------------
# 1. Load Dataset & Index
# ------------------------
print("🔄 Loading model and index...")

# Load docs
with open("medquad_docs.pkl", "rb") as f:
    docs = pickle.load(f)

# Load FAISS index
index = faiss.read_index("medquad_faiss.index")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("✅ Model & index loaded successfully")

# ------------------------
# 2. FastAPI Setup
# ------------------------
app = FastAPI(title="Medical Q&A Chatbot",
              description="AI-powered assistant using MedQuAD dataset",
              version="1.0")

class Query(BaseModel):
    question: str
    top_k: int = 3

# ------------------------
# 3. Chatbot Function
# ------------------------
def medical_chatbot(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [docs[idx] for idx in indices[0]]
    
    best_answer = results[0]["a"]
    
    return {
        "user_question": query,
        "assistant_answer": best_answer,
        "retrieved_questions": [r["q"] for r in results]
    }

# ------------------------
# 4. API Endpoint
# ------------------------
@app.post("/ask")
def ask_medical_qna(query: Query):
    response = medical_chatbot(query.question, query.top_k)
    return response

# ------------------------
# 5. Run with:
# uvicorn app:app --reload
# ------------------------
