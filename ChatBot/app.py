import streamlit as st
from chatbot import get_response

st.title("Chat-Bot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.chat_input("Ask anything......")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

        st.session_state['messages'].append({
            'role':"user",
            'content':user_input
        })

    response = get_response(st.session_state['messages'])

    with st.chat_message("ai"):
        st.write(response)

        st.session_state['messages'].append({
            'role':"ai",
            'content':response
        })