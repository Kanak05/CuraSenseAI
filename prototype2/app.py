import streamlit as st
import requests
import textwrap
import json
from datetime import datetime

# --- App Configuration ---
st.set_page_config(page_title="CuraSense AI - Medical Health Assistant", page_icon="🩺", layout="wide")

# --- Backend API URL ---
# IMPORTANT: Replace this with the public ngrok URL from your Colab notebook output
COLAB_API_URL = "https://262676452d66.ngrok-free.app/ask" # Replace with your actual ngrok URL

# --- Enhanced Sidebar ---
with st.sidebar:
    st.title("🩺 CuraSense AI")
    
    # NEW: New Chat button (replaces "Clear Chat")
    if st.button("➕ New Chat"):
        # Before starting a new chat, save the old one to history if it has content
        if len(st.session_state.get("messages", [])) > 1:
             if "chat_history" not in st.session_state:
                 st.session_state.chat_history = []
             # Add timestamp to saved chat
             chat_data = {
                 "messages": list(st.session_state.messages),
                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "summary": next((msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content'] 
                                for msg in st.session_state.messages if msg['role'] == 'user'), "Conversation")
             }
             st.session_state.chat_history.insert(0, chat_data)
        
        # Reset the current chat
        st.session_state.messages = [{"role": "assistant", "content": "New chat started. How can I help you?"}]
        st.rerun()

    st.subheader("Chat History")

    # NEW: Search bar for chat history
    search_term = st.text_input("🔍 Search history...", key="search_history").lower()

    # Initialize chat_history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Filter history based on the search term
    if search_term:
        filtered_history = [
            chat for chat in st.session_state.chat_history
            if any(search_term in message['content'].lower() for message in chat["messages"])
        ]
    else:
        filtered_history = st.session_state.chat_history

    # NEW: Display chat history items as buttons
    if not filtered_history:
        st.info("No past conversations found.")
    else:
        # Display the newest conversations first
        for i, chat_data in enumerate(filtered_history):
            # Use the first user prompt as the button label, truncated for brevity
            try:
                # Safely extract time from timestamp
                timestamp_parts = chat_data['timestamp'].split()
                time_part = timestamp_parts[1][:5] if len(timestamp_parts) > 1 else chat_data['timestamp'][:10]
                button_label = f"📜 {chat_data['summary']} ({time_part})"
            except (IndexError, KeyError):
                # Fallback if timestamp format is unexpected
                button_label = f"📜 {chat_data['summary']}"
            
            if st.button(button_label, key=f"history_{i}"):
                # When a history button is clicked, load that chat into the main window
                st.session_state.messages = chat_data["messages"]
                st.rerun()

    # NEW: Clear History button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()

    # NEW: Export Chats button
    if st.session_state.chat_history:
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_conversations": len(st.session_state.chat_history),
            "conversations": st.session_state.chat_history
        }
        export_json = json.dumps(export_data, indent=2)
        
        st.download_button(
            label="📤 Export Chats",
            data=export_json,
            file_name=f"curasense_chats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    # NEW: Important Notice
    st.subheader("⚠️ Important Notice")
    st.error("**Medical Disclaimer:** I am an AI assistant and not a medical professional. Please consult a doctor for any health concerns.")
    
    st.warning("Always consult a healthcare professional for medical advice.", icon="⚠️")

    # NEW: About section
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        **CuraSense AI** is a helpful assistant designed to make medical information more accessible and understandable. 
        It uses a powerful AI model grounded in a curated knowledge base to answer your health questions accurately and safely.
        """)
        st.markdown("""
        **How to Use:**
        1.  Type your health-related question in the chat box.
        2.  Press Enter to get an answer.
        3.  Use the buttons and features in the sidebar to manage your conversations.
        """) 
        
# --- Main App Logic (No changes needed here) ---
st.title("🩺 CuraSense AI - Medical Health Assistant")
st.warning("**Disclaimer:** I am an AI assistant and not a medical professional. Please consult a doctor for any health concerns.", icon="⚠️")

# Initialize chat history if it doesn't exist (for the very first run)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you?"}]

# Display current chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the Colab backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(COLAB_API_URL, json={"question": prompt}, timeout=300)
                response.raise_for_status()
                
                answer = response.json().get("answer", "Sorry, something went wrong.")
                formatted_answer = answer.replace("\n", "  \n")
                
                st.markdown(formatted_answer)
                st.session_state.messages.append({"role": "assistant", "content": formatted_answer})

            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend: {e}")