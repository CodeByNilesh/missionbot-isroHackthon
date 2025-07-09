# app.py

import streamlit as st
from chatbot_engine import load_knowledge_base, build_faiss_index, search_answer

st.set_page_config(page_title="MissionBot", page_icon="🚀")

st.title("MissionBot: Your AI Assistant for Space Missions 🚀")

with st.spinner("Loading knowledge base..."):
    questions, answers = load_knowledge_base()
    model, index, embeddings = build_faiss_index(questions)

user_query = st.text_input("🔍 Ask me a question:", key="input")

if user_query:
    with st.spinner("Thinking... 🤖"):
        response = search_answer(user_query, model, index, questions, answers, embeddings)
    st.success(response)