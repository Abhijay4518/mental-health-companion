import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mental Health Companion", page_icon="🧠")

st.title("🧠 AI Mental Health Companion")
st.markdown("A safe space to express your feelings 💙")

API_KEY = st.secrets["OPENROUTER_API_KEY"]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def generate_response(user_input):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a compassionate mental health support chatbot."},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    return result["choices"][0]["message"]["content"]

user_input = st.text_area("💬 How are you feeling today?")

if st.button("Send") and user_input:
    try:
        reply = generate_response(user_input)
        
        st.session_state.chat_history.append({
            "time": datetime.now().strftime("%H:%M"),
            "user": user_input,
            "bot": reply
        })
    except Exception as e:
        st.error(str(e))

st.subheader("Chat History")

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**🕒 {chat['time']}**")
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**AI:** {chat['bot']}")
    st.markdown("---")

