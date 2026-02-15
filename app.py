import streamlit as st
from google import genai
from datetime import datetime

st.set_page_config(page_title="Mental Health Companion", page_icon="🧠", layout="wide")

st.title("🧠 AI Mental Health Companion")
st.markdown("A safe, supportive space for students to express emotions and receive guidance.")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
MODEL_NAME = "gemini-1.5-flash-latest"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def detect_mood(text):
    prompt = f"""
    Analyze the emotional tone of this text.
    Classify it into ONE word only from:
    Happy, Sad, Anxious, Stressed, Angry, Depressed, Neutral.

    Text: {text}
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()

def generate_response(text, mood):
    prompt = f"""
    You are a compassionate AI mental health companion.

    The student feels: {mood}
    Student message: {text}

    Provide:
    1. An empathetic response
    2. A short motivational encouragement
    3. Two practical relaxation techniques
    4. A gentle reminder to seek professional help if needed

    Keep tone warm and supportive.
    Avoid medical diagnosis.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

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

user_input = st.text_area("💬 How are you feeling today?")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter your thoughts.")
    else:
        if check_crisis(user_input):
            st.error("🚨 If you are in immediate danger, please contact emergency services.")
            st.info("India Mental Health Helpline: 📞 9152987821")
        else:
            mood = detect_mood(user_input)
            reply = generate_response(user_input, mood)

            st.session_state.chat_history.append({
                "time": datetime.now().strftime("%H:%M"),
                "user": user_input,
                "mood": mood,
                "bot": reply
            })

st.subheader("🗂 Chat History")

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**🕒 {chat['time']}**")
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Detected Mood:** *{chat['mood']}*")
    st.markdown(f"**AI Companion:** {chat['bot']}")
    st.markdown("---")
