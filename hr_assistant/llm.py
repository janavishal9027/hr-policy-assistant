""" Connect to LLM API(Brain) and get response from it. """

from langchain_groq import ChatGroq
from hr_assistant import config

def get_llm_response():
    """Get response from LLM API(Brain) using the provided prompt and configuration."""
    llm = ChatGroq(
        model=config.LLM_MODEL_NAME,
        temperature=0.9,
    )
    return llm