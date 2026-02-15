import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Working Test")

st.title("Gemini Working Test")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

if st.button("Test Gemini"):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say hello in one short sentence."
        )
        st.success(response.text)
    except Exception as e:
        st.error(f"ERROR: {e}")

