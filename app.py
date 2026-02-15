import streamlit as st
from datetime import datetime
from textblob import TextBlob
import random

st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="🧠",
    layout="centered"
)
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.main {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 15px;
}
.stTextArea textarea {
    border-radius: 10px;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #45a049;
}
.chat-box {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}
.user-msg {
    background-color: #e3f2fd;
    color: black;
}
.bot-msg {
    background-color: #f1f8e9;
    color: black;
}
.mood-tag {
    font-size: 12px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Mental Health Companion")
st.markdown("A safe, supportive space for students to express emotions and receive guidance 💙")
st.markdown("---")
st.caption("⚠ This AI tool provides supportive guidance but is not a replacement for professional mental health care.")
st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def check_crisis(text):
    crisis_keywords = [
        "suicide",
        "kill myself",
        "end my life",
        "self harm",
        "die",
        "hopeless",
        "worthless"
    ]
    for word in crisis_keywords:
        if word in text.lower():
            return True
    return False
def detect_mood(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return "Happy 😊"
    elif polarity > 0:
        return "Neutral 🙂"
    elif polarity > -0.3:
        return "Sad 😔"
    else:
        return "Depressed 💔"
def generate_response(mood):
    responses = {
        "Happy 😊": [
            "I'm so glad you're feeling positive! Keep nurturing that energy 🌟",
            "That’s wonderful to hear! Keep spreading that positivity!"
        ],
        "Neutral 🙂": [
            "It’s okay to have balanced days. How can I support you today?",
            "Thanks for sharing. Even neutral days matter."
        ],
        "Sad 😔": [
            "I’m really sorry you're feeling this way. You're not alone.",
            "It’s okay to feel sad sometimes. Take things one step at a time."
        ],
        "Depressed 💔": [
            "I’m really sorry you're going through this. Please consider speaking with someone you trust.",
            "Your feelings matter. Reaching out to a professional could really help."
        ]
    }
    return random.choice(responses[mood])
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("💬 How are you feeling today?", height=120)
    submitted = st.form_submit_button("Send Message")

if submitted and user_input:

    if check_crisis(user_input):
        st.error("🚨 If you are in immediate danger, please contact emergency services.")
        st.info("India Mental Health Helpline: 📞 9152987821")
    else:
        mood = detect_mood(user_input)
        reply = generate_response(mood)

        st.session_state.chat_history.append({
            "time": datetime.now().strftime("%H:%M"),
            "user": user_input,
            "mood": mood,
            "bot": reply
        })

st.subheader("🗂 Conversation History")

for chat in reversed(st.session_state.chat_history):

    st.markdown(f"""
    <div class="chat-box user-msg">
        <b>You:</b> {chat['user']}<br>
        <span class="mood-tag">Detected Mood: {chat['mood']}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chat-box bot-msg">
        <b>AI Companion:</b><br>
        {chat['bot']}
    </div>
    """, unsafe_allow_html=True)


