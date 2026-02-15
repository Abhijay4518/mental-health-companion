import streamlit as st
from google import genai

st.title("Gemini Free Tier Test")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

if st.button("Test Gemini"):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents="Say hello in one short sentence."
        )
        st.success(response.text)
    except Exception as e:
        st.error(str(e))

