import streamlit as st
from translation import get_translation
from langchain_openai import OpenAI
from langchain_mistralai.chat_models import ChatMistralAI

import os
from dotenv import load_dotenv


load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
supabase_url = os.getenv('SUPABASE_URL')
supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY')
mistral_api_key = os.getenv('MISTRAL_API_KEY')


def main():
    langbutton = st.sidebar.selectbox(
        "language :",
        ("Français", "Nederlands", "English")
    )

    strings = get_translation(langbutton)

    st.title(strings["title"])
    st.image("logo.png", width=200)

    if 'modelmemory' not in st.session_state:
        st.session_state['modelmemory'] = []

    modelbutton = st.sidebar.selectbox(strings["select_model"],
        ("gpt-3.5-turbo", "Mistral 7B"),
    )

    if modelbutton not in st.session_state['modelmemory']:
        st.session_state['modelmemory'].append(modelbutton)

    temperature = st.sidebar.slider(
        label="select temperature", min_value=0.1, max_value=0.8, value=0.3, step=0.1
    )

    if 'temperaturememory' not in st.session_state:
        st.session_state['temperaturememory'] = []

    st.session_state['temperaturememory'].append(temperature)

    if modelbutton == "gpt-3.5-turbo":
        llm = OpenAI(temperature=temperature, max_tokens=400, api_key=openai_api_key)
    elif modelbutton == "Mistral 7B":
        llm = ChatMistralAI(temperature=temperature, mistral_api_key=mistral_api_key)

if __name__ == "__main__":
    main()
