""" Connect to LLM API(Brain) and get response from it. """

from langchain_groq import ChatGroq
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_llm_response():
    """Get response from LLM API(Brain) using the provided prompt and configuration."""
    logger.info(f"Initializing LLM with model name: {config.LLM_MODEL_NAME}")
    llm = ChatGroq(
        model=config.LLM_MODEL_NAME,
        temperature=0.9,
    )
    return llm