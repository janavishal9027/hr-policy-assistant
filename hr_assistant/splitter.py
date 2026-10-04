"""Chop the text into smaller chunks for processing."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def split_text_into_chunks(documents):
    """Split the document into smaller chunks based on the configuration settings."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.CHUNK_SIZE,
        chunk_overlap = config.CHUNK_OVERLAP,
    )
    chunks = text_splitter.split_documents(documents)  # Return the list of document chunks
    logger.info(f"Splitting documents into chunks of size {config.CHUNK_SIZE} with overlap {config.CHUNK_OVERLAP}")
    return chunks