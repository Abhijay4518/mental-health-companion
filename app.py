import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Free Test")

st.title("Gemini Free Tier Test")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

if st.button("Test Gemini"):
    try:
        response = model.generate_content("Say hello in one short sentence.")
        st.success(response.text)
    except Exception as e:
        st.error(str(e))
))

