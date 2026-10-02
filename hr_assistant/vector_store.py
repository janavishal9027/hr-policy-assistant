"""Store the Chunk embeddings data in FAISS database so that it can be searched later for relevant information based on the user query."""

import os
from langchain_community.vectorstores import FAISS
from hr_assistant import config
from hr_assistant.embeddings import get_embedding_model

# Building vector store using FAISS and Jina embeddings

def build_vector_store(chunks):
    """Build a FAISS vector store from the provided documents using Jina embeddings."""
    embedding_model = get_embedding_model()  # Get the embedding model
    return FAISS.from_documents(chunks, embedding_model)  # Create a FAISS vector store from the Chunks and embeddings

# Saving and loading the vector store

def save_vector_store(vector_store, path: str=config.VECTOR_STORE_PATH) -> None:
    """Save the FAISS vector store to the specified path."""
    os.makedirs(path, exist_ok=True)  # Create the directory if it doesn't exist
    vector_store.save_local(path)  # Save the vector store locally

def load_vector_store(path: str =config.VECTOR_STORE_PATH):
    """Load the FAISS vector store from the specified path."""
    return FAISS.load_local(path, get_embedding_model(), allow_dangerous_deserialization=True)  # Load the vector store locally

# Check if the vector store exists

def vector_store_exists(path: str = config.VECTOR_STORE_PATH) -> bool:
    """Check if the FAISS vector store exists at the specified path."""
    return os.path.exists(os.path.join(path, "index.faiss"))  # Return True if the path exists, otherwise False

# Get a retriever from the vector store

def get_retriever(vector_store, k: int = config.TOP_K_RESULTS):
    """Turn a vector store into a retriever that returns the top-k matching chunks for searching relevant information."""
    return vector_store.as_retriever(search_kwargs={"k": k})  # Return a retriever with the specified number of top results

