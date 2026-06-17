import google.generativeai as genai
from tools import search_web
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_ai(question):

    if (
        "latest" in question.lower()
        or
        "news" in question.lower()
        or
        "current" in question.lower()
    ):

        web_data = search_web(question)

        prompt = f"""
Use this data:

{web_data}

Question:

{question}
"""

    else:

        prompt = question

    response = model.generate_content(
        prompt
    )

    return response.text