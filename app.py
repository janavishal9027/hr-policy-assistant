"""
Streamlit chat app for the HR Assistant. 

This is the entry point for the Streamlit application, which provides a user-friendly interface for interacting with the HR Assistant agent.

It orchestrates the entire process, from loading the HR policy documents, creating embeddings, storing them in a vector store, and setting up the agent to answer user queries.
"""


import streamlit as st
from hr_assistant.pipeline import ask, build_hr_assistant_agent

st.set_page_config(page_title="HR PolicyAssistant", page_icon="🤖")
st.title("🤖 HR Policy Assistant")
st.caption("Ask me anything about company's HR policies and get instant answers!")


@st.cache_resource(show_spinner="Setting up the assistant (only happens once)...")
def get_agent():
    """Build the HR Assistant agent and cache it for future use."""
    return build_hr_assistant_agent()  # Build the HR Assistant agent

agent = get_agent()  # Get the HR Assistant agent

if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize the message history in the session state

# Show the chat history on the Streamlit app

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  # Display the message content in the chat

# get a new question from the user
question = st.chat_input("Ask me anything about company's HR policies...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})  # Add the user's question to the message history
    with st.chat_message("user"):
        st.markdown(question)  # Display the user's question in the chat

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask(agent, question)  # Ask the question to the agent
        st.markdown(answer)  # Display the agent's answer in the chat
    st.session_state.messages.append({"role": "assistant", "content": answer})  # Add the agent's answer to the message history