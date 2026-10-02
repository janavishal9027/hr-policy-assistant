""" Turn the HR policy documents text into number (Vectors) using Jina embeddings. """

from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config

def get_embedding_model():
    """Get the Jina embedding model using the API key from the configuration."""
    return JinaEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME
    )