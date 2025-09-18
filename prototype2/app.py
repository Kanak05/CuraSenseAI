import streamlit as st
import requests
import textwrap

# --- App Configuration ---
st.set_page_config(page_title="CuraSence AI - Medical Health Assistant", page_icon="🩺", layout="wide")

# --- Backend API URL ---
# IMPORTANT: Replace this with the public ngrok URL from your Colab notebook output
COLAB_API_URL = "https://0ddb5af31f39.ngrok-free.app/ask"

# --- Main App Logic ---

# Title and Disclaimer
st.title("🩺 CuraSence AI - Medical Health Assistant")
# st.info("This frontend is powered by a backend running on Google Colab with a GPU.")
st.warning("**Disclaimer:** I am an AI assistant and not a medical professional. Please consult a doctor for any health concerns.", icon="⚠️")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a health question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the Colab backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(COLAB_API_URL, json={"question": prompt}, timeout=300)
                response.raise_for_status() # Raise an exception for bad status codes
                
                answer = response.json().get("answer", "Sorry, something went wrong.")
                
                formatted_answer = answer.replace("\n", "  \n")
                
                st.markdown(formatted_answer)
                
                st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
                
                
                
                
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend: {e}")