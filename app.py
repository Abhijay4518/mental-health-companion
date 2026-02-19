import streamlit as st
import requests
from datetime import datetime
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Mental Health & Student Wellness Companion",
    page_icon="🧠",
    layout="centered"
)
st.markdown("""
<style>
.chat-box {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: black;
}
.user-msg {
    background-color: #e3f2fd;
}
.bot-msg {
    background-color: #f1f8e9;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.title("🎓 Student Wellness Companion")
section = st.sidebar.radio(
    "Navigate",
    ["Mental Support Chat", "Student Wellness", "Chat History"]
)

st.sidebar.markdown("---")
st.sidebar.success("App Status: Live & Operational ✅")

API_KEY = st.secrets["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"]

def call_ai(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]

def generate_ai_response(user_input):

    system_prompt = """
    You are a compassionate AI Student Wellness Companion.
    Support students facing stress, anxiety, or academic pressure.
    Respond in a calm, empathetic, and motivating tone.
    Encourage balance between studies and mental health.
    Avoid medical diagnosis and suggest seeking help if needed.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    return call_ai(messages)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def check_crisis(text):
    keywords = ["suicide", "kill myself", "end my life", "self harm", "hopeless"]
    return any(word in text.lower() for word in keywords)

def detect_mood(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return "Happy 😊"
    elif polarity > 0:
        return "Neutral 🙂"
    elif polarity > -0.3:
        return "Sad 😔"
    else:
        return "Depressed 💔"

if section == "Mental Support Chat":

    st.title("🧠 AI Mental Health Companion")
    st.markdown("Express your feelings safely 💙")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("💬 How are you feeling today?", height=120)
        submitted = st.form_submit_button("Send Message")

    if submitted and user_input:

        if check_crisis(user_input):
            st.error("🚨 Please seek immediate professional help.")
            st.info("India Helpline: 📞 9152987821")
        else:
            mood = detect_mood(user_input)
            reply = generate_ai_response(user_input)

            st.session_state.chat_history.append({
                "time": datetime.now().strftime("%H:%M"),
                "user": user_input,
                "mood": mood,
                "bot": reply
            })

    st.subheader("🗂 Conversation")

    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div class="chat-box user-msg">
            <b>You:</b> {chat['user']}<br>
            <small>Mood: {chat['mood']}</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="chat-box bot-msg">
            <b>AI:</b><br>
            {chat['bot']}
        </div>
        """, unsafe_allow_html=True)
    if st.session_state.chat_history:
        moods = [chat["mood"] for chat in st.session_state.chat_history]
        mood_counts = pd.Series(moods).value_counts()

        st.subheader("📊 Mood Analytics")
        fig, ax = plt.subplots()
        mood_counts.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.subheader("📈 Mood Trend")
        mood_map = {"Happy 😊": 3, "Neutral 🙂": 2, "Sad 😔": 1, "Depressed 💔": 0}
        numeric = [mood_map.get(m, 2) for m in moods]
        trend_df = pd.DataFrame({"Entry": range(1, len(numeric)+1), "Mood Level": numeric})
        st.line_chart(trend_df.set_index("Entry"))

if section == "Student Wellness":

    st.title("📊 Student Wellness Tracker")

    study = st.slider("📚 Study Hours", 0, 12, 2)
    sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
    stress = st.slider("😰 Stress Level (0-10)", 0, 10, 5)

    if st.button("Analyze Wellness"):
        prompt = f"Study: {study} hrs, Sleep: {sleep} hrs, Stress: {stress}/10. Provide short wellness advice."
        reply = generate_ai_response(prompt)
        st.write(reply)

    data = pd.DataFrame({
        "Metric": ["Study", "Sleep", "Stress"],
        "Value": [study, sleep, stress]
    })

    st.bar_chart(data.set_index("Metric"))

if section == "Chat History":

    st.title("🗂 Previous Chats")

    if not st.session_state.chat_history:
        st.warning("No chat history available.")
    else:
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div class="chat-box user-msg">
                <b>{chat['time']}</b><br>
                {chat['user']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="chat-box bot-msg">
                {chat['bot']}
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑 Clear History"):
            st.session_state.chat_history = []
            st.success("History Cleared")




