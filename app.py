import streamlit as st
import requests
import uuid
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
API_KEY = os.getenv("ANYTHINGLLM_API_KEY")
BASE_URL = os.getenv("ANYTHINGLLM_URL", "http://localhost:3001/api/v1")
WORKSPACE_SLUG = os.getenv("WORKSPACE_SLUG", "my-workspace")
HISTORY_FILE = "chat_history.json"

st.set_page_config(page_title="AI Agent Terminal", layout="wide")


# --- DATA PERSISTENCE ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# --- UPLOAD FUNCTION ---
def upload_document(uploaded_file):
    url = f"{BASE_URL}/document/upload"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            doc_data = response.json().get('documents', [{}])[0]
            location = doc_data.get('location')
            move_url = f"{BASE_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings"
            move_payload = {"adds": [location]}
            requests.post(move_url, headers=headers, json=move_payload)
            return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
    return False


# --- AI SUMMARIZER ---
def get_chat_summary(first_prompt):
    payload = {"message": f"Summarize this into a 3-word title: {first_prompt}", "mode": "chat"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.post(f"{BASE_URL}/workspace/{WORKSPACE_SLUG}/chat",
                                 json=payload, headers=headers)
        return response.json().get('textResponse', "New Chat")[:30].replace('"', '')
    except:
        return first_prompt[:20] + "..."


# --- STATE INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = load_history()
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("Conversations")
    if st.button("+ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.history[new_id] = {"title": "Empty Chat", "messages": []}
        st.session_state.current_chat_id = new_id
        save_history(st.session_state.history)

    st.divider()

    for chat_id in list(st.session_state.history.keys()):
        cols = st.columns([0.8, 0.2])
        if cols[0].button(st.session_state.history[chat_id]["title"], key=f"s_{chat_id}", use_container_width=True):
            st.session_state.current_chat_id = chat_id
        if cols[1].button("🗑️", key=f"d_{chat_id}"):
            del st.session_state.history[chat_id]
            save_history(st.session_state.history)
            st.rerun()

# --- MAIN INTERFACE ---
if st.session_state.current_chat_id:
    cid = st.session_state.current_chat_id
    chat = st.session_state.history[cid]

    st.subheader(chat["title"])

    # Display message history
    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # --- ATTACHMENT POPOVER (Keeps Chat Input Pinned) ---
    st.write("")  # Small spacer
    with st.popover("➕ Attach Document"):
        uploaded_file = st.file_uploader("Select file", type=['pdf', 'txt', 'docx'], label_visibility="collapsed")
        if uploaded_file:
            with st.spinner("Uploading..."):
                if upload_document(uploaded_file):
                    st.success(f"'{uploaded_file.name}' attached successfully!")

    # --- CHAT INPUT (Root level to stay at bottom) ---
    if prompt := st.chat_input("Command agent..."):
        chat["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner(""):
                headers = {"Authorization": f"Bearer {API_KEY}"}
                # Changed mode to 'chat' to stop the workspace empty errors
                payload = {"message": f"@agent {prompt}", "mode": "chat", "sessionId": cid}
                response = requests.post(f"{BASE_URL}/workspace/{WORKSPACE_SLUG}/chat",
                                         json=payload, headers=headers)

                if response.status_code == 200:
                    ans = response.json().get('textResponse', "")
                    st.write(ans)
                    chat["messages"].append({"role": "assistant", "content": ans})

                    if len(chat["messages"]) == 2:
                        chat["title"] = get_chat_summary(prompt)

                    save_history(st.session_state.history)
                    st.rerun()
                else:
                    st.error("Error communicating with AnythingLLM.")
else:
    st.info("Start a new conversation to begin.")