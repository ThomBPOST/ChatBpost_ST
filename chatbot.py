# PC    : streamlit run ChatBpost_ST/chatbot.py
# Linux : streamlit run /home/thomas/Documents/bpostchatbot/chatbot.py


#TODOLIST : 

'''
- Filtrer prompt en fonction des metas datas
- Reset la taille des msgs pour ne pas atteindre les 4k
- https://brain.d.foundation/Engineering/AI/Workaround+with+OpenAI%27s+token+limit+with+Langchain
- https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache cache streamlit
- Traduire les nouveaux outils et les ajouter dans le .py translation
- Ajouter/modifier l'api mistral.ai avec la doc https://docs.mistral.ai/platform/client/
- Option Regénération des vecteurs (prio basse)
- Regarder secret manager sur streamlit
- share le streamlit publiquement
- FAIRE HYPER ATTENTION QU'IL N'Y A PAS DE CLE D'API

'''

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.messages import BaseMessage





preprompt =(
        "Tu es un assistant pour les team leaders chez bpost pendant la période des élections. "
        "Réponds à la question de l'utilisateur en utilisant les informations qui te sont fournies. "
        "Si tu ne trouves pas les informations, dites-le à l'utilisateur et que tu es là pour répondre aux questions "
        "sur les process de bpost pour les élections en Belgique. Essaye de répondre un maximum sur base des documents "
        "que je t'ai fourni et n'invente pas de nouveaux éléments. Répond toujours dans la langue de la question de l'utilisateur. "
        "Lorsqu'on te pose une question sur un process, je veux que tu mettes TOUTES les étapes dans la réponse, avec les marches à suivre et les remarques importantes si il y en a, de manière structurée avec des retours à la lignes si il faut. "
        "Quand on te demande la définition ou la signification d'un mot, répond d'un phrase courte et simple, et ou d'exemples. Donne juste la signification du mot."
        " Si tu reçois un message qui n'a aucun sens, répond simplement : Je ne comprend pas votre question ." 
        " Si le 'type': 'Lexique', alors répond de la manière la plus brève possible en restant proche de la définition du document."
        " Si le 'type': 'SOP', alors répond en donnant les étapes du documents. Il faut que la personne comprennent toutes les étapes "
        " Si le 'type': 'Text', je veux que tu répondes de la manière la plus brève possible en maximum 2 ou 3 phrases. "
)



st.title("chatbot election")

st.image("logo.png", width=200)



with st.sidebar:
    # Demander la clé API à l'utilisateur
    openai_api_key_input = st.text_input("OpenAI API Key", key="input_openai_api_key", type="password")
    st.write("Put your OpenAI key. Do not share it!")  # Rappel de sécurité

    # Stocker la clé API dans session_state si elle est saisie
    if openai_api_key_input:
        openai_api_key = openai_api_key_input
        activated = True
    else:
        activated = False
        
if activated:
    # Création des instances en utilisant la clé API stockée
    msgs = StreamlitChatMessageHistory(key = 'chat_message_history')
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    llm = OpenAI(temperature=0.3, max_tokens=400, openai_api_key=openai_api_key)

    # Vos autres initialisations dépendantes de la clé API
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_service_key = st.secrets["SUPABASE_SERVICEKEY"]
    supabase = create_client(supabase_url, supabase_service_key)

    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system",preprompt),
        MessagesPlaceholder(variable_name="history"), 
        ("human", "{question}"),

    ]
    )

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
    )

    if 'chat_message_history' not in st.session_state:
        st.session_state['chat_message_history'] = []





    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",preprompt()),
            MessagesPlaceholder(variable_name="history"), 
            ("human", "{question}"),

        ]
    )

    #Petit snippet pour afficher le chunk sur lequel on travaille
    if 'context_retrieval' not in st.session_state:
        st.session_state['context_retrieval'] = []

    
    if len(msgs.messages) >= 500:
        # Vider la liste des messages
        msgs.messages.clear()

    if len(msgs.messages) == 0:
        msgs.add_ai_message("AI : Hello !")


    for msg in msgs.messages:
        # Split and display only the part before "[Document(page_content..."
        if msg.type == "human":
            # Find the index where "[Document(page_content..." starts
            doc_start_index = msg.content.find("[Document(page_content")
            # If the substring is found, split the content and display only the part before it
            if doc_start_index != -1:
                content_parts = msg.content.split("[Document(page_content", 1)
                content_to_display = content_parts[0]
            else:
                content_to_display = msg.content
            st.chat_message(msg.type).write(content_to_display)
        else:
            st.chat_message(msg.type).write(msg.content)



    if prompt := st.chat_input():
        # Perform context retrieval separately without altering the original prompt
        context_retrieval = retriever.vectorstore.similarity_search(prompt, k = 1)
        st.session_state['context_retrieval'].append(context_retrieval)  # Stocker le chunk que le retrieval est parti cherché 
        # Log the human message as it is
        st.chat_message("human").write(prompt)
        config = {"configurable": {"session_id": "any"}}
        # Invoke the chain with the original prompt and handle context_retrieval separately as needed
        every_context = prompt + str(context_retrieval)
        response = chain_with_history.invoke({"question": every_context}, config)  # context_retrieval handled internally if necessary
        st.chat_message("ai").write(response)


    cleaned_messages = []
    for msg in msgs.messages:
        # Trouver l'indice où "[Document(page_content" commence et le supprimer
        doc_start_index = msg.content.find("[Document(page_content")
        if doc_start_index != -1:
            # Supprimer le contenu après l'indice trouvé
            msg.content = msg.content[:doc_start_index]

        if msg.content.strip():  # Cette vérification s'assure que le contenu n'est pas uniquement composé d'espaces
            
            cleaned_messages.append(msg)

    st.session_state['chat_message_history'] = msgs.messages





