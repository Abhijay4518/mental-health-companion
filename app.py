import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Test")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Gemini Test App")

if st.button("Test Gemini"):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Say hello in one sentence."
    )
    st.write(response.text)


