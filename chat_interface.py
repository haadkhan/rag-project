import streamlit as st
from src.rag import RAG
from src.generate import llm_caller

# Instantiate objects once outside the loop for better performance
if "rag" not in st.session_state:
    st.session_state.rag = RAG()
if "client" not in st.session_state:
    st.session_state.client = llm_caller()

st.title("RAG Chat Interface")

# Maintain conversation session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Question for RAG?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    context = st.session_state.rag.retrieve_and_augment(prompt)
    full_response = st.session_state.client.generate(prompt, context)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(full_response)
    
    # Append the final complete string to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})