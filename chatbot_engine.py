import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def load_knowledge_base(file_path="data/knowledge_base.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]
    return questions, answers

def build_faiss_index(questions, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name, device="cpu")
    embeddings = model.encode(questions)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return model, index, embeddings

def search_answer(query, model, index, questions, answers, embeddings, threshold=0.75):
    query_vector = model.encode([query])
    D, I = index.search(query_vector, 1)
    distance = D[0][0]
    best_idx = I[0][0]

    if distance > threshold:
        return "🤖 I'm not sure how to answer that yet. Try asking about space missions or global science topics!"
    else:
        return answers[best_idx]
