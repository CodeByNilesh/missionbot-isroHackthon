import streamlit as st

st.set_page_config(page_title="MissionBot 🛰️", layout="centered")

st.title("🚀 MissionBot")
st.subheader("Chatbot for ISRO Missions & Pollution Awareness")

user_input = st.text_input("Ask a question:")
if user_input:
    st.write("You asked:", user_input)
    st.info("🤖 I'm still learning how to answer that. Stay tuned!")
