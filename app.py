"""
Streamlit chat app for the HR Assistant. 

This is the entry point for the Streamlit application, which provides a user-friendly interface for interacting with the HR Assistant agent.

It orchestrates the entire process, from loading the HR policy documents, creating embeddings, storing them in a vector store, and setting up the agent to answer user queries.
"""


import streamlit as st
from hr_assistant.pipeline import (
    ask,
    ask_stream,
    build_hr_assistant_agent
)

from hr_assistant.logger import get_logger

logger = get_logger(__name__)

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# APPLICATION HEADER
# ============================================================
st.title("🤖 HR Policy Assistant")
st.caption(
    "Ask me anything about company's HR policies "
    "and get instant answers!"
)

# ============================================================
# BUILD / LOAD AGENT
# ============================================================

@st.cache_resource(
    show_spinner="Setting up the assistant (only happens once)..."
)
def get_agent():
    """
    Build the HR Assistant agent and cache it.

    The agent will only be created once during the Streamlit
    session unless the cache is cleared.
    """

    return build_hr_assistant_agent()


agent = get_agent()


# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================
if "messages" not in st.session_state:

    st.session_state.messages = []

# ============================================================
# DISPLAY PREVIOUS CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# ============================================================
# CHAT INPUT
# ============================================================
question = st.chat_input(
    "Ask me anything about company's HR policies..."
)

# ============================================================
# PROCESS NEW QUESTION
# ============================================================

if question:

    logger.info(
        "=== Streamlit run: new question received ==="
    )

    logger.info(
        f"User question: {question}"
    )

    # --------------------------------------------------------
    # Add user message to session history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------------------------
    # Generate assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            # Stream response word-by-word
            answer = st.write_stream(
                ask_stream(
                    agent,
                    question
                )
            )

        except Exception as e:

            logger.exception(
                "Error while generating streaming response."
            )

            answer = (
                "Sorry, I encountered an error while "
                "processing your request."
            )

            st.error(
                f"Error: {str(e)}"
            )

    # --------------------------------------------------------
    # Save completed assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    logger.info(
        f"Completed assistant response: {answer}"
    )