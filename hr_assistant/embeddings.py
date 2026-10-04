""" Turn the HR policy documents text into number (Vectors) using Jina embeddings. """

from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_embedding_model():
    """Get the Jina embedding model using the API key from the configuration."""
    logger.info(f"Initializing Jina embedding model with model name: {config.EMBEDDING_MODEL_NAME}")
    return JinaEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME
    )