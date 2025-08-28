import streamlit as st
import requests

# ------------------------
# Streamlit Page Setup
# ------------------------
st.set_page_config(page_title="CuraSense AI - Medical Q&A", page_icon="🩺")
st.title("🩺 CuraSense AI - Medical Q&A Chatbot")
st.markdown("Ask your health-related questions. (⚠️ Not a substitute for medical advice)")

# ------------------------
# API Endpoint
# ------------------------
API_URL = "http://127.0.0.1:8000/ask"   # FastAPI backend URL

# ------------------------
# Chat UI
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Input box for new question
if prompt := st.chat_input("Type your medical question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Send to FastAPI backend
    try:
        response = requests.post(API_URL, json={"question": prompt})
        if response.status_code == 200:
            answer = response.json()["assistant_answer"]
        else:
            answer = "⚠️ Error: Could not connect to backend."
    except Exception as e:
        answer = f"⚠️ Exception: {e}"

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").markdown(answer)
