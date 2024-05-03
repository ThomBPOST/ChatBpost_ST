import streamlit as st




def show_debug_info(debug_button, msgs):
    if debug_button:
        with st.expander("Mode DEBUG"):
            # Affichage des informations de débogage HISTORIQUE COMPLET
            st.write("**Chat History** \n \n " + str(msgs))  
            # st.write("**Temperature History** \n \n " + str(st.session_state['temperaturememory']))
            # st.write("**Model History** \n \n " + str(st.session_state['modelmemory']))
            last_temperature = st.session_state['temperaturememory'][-1] if st.session_state['temperaturememory'] else "No temperatures yet"
            last_model = st.session_state['modelmemory'][-1] if st.session_state['modelmemory'] else "No models yet"
            last_message = st.session_state['chat_message_history'][-1] if st.session_state['chat_message_history'] else "No messages yet"
            last_chunk = st.session_state['context_retrieval'][-1] if st.session_state['context_retrieval'] else "No context retrieval yet"

            st.write(f"**Last Temperature:** {last_temperature}")
            st.write(f"**Last Model Used:** {last_model}")
            st.write(f"**Last Message AI:** {last_message}")
            st.write(f"**Last Context Retrieval:** {last_chunk}")


    


