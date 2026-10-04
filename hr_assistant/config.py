import os
from dotenv import load_dotenv

load_dotenv()

# Access API keys from environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Tracing and logging configuration for LangChain
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

## Define path - Data / Vector Store

DATA_PATH = os.path.join("hr_policy", "policy_documents.txt")  # Path to the HR policy documents

## Vector Store

# In Memory Vector Store
# Persistent Vector Store
# Cloud memory store


VECTOR_STORE_PATH = os.path.join("hr_policy", "faiss_index")  # Path to the vector store for storing embeddings

# Models
# LLM Models and Embedding Models

LLM_MODEL_NAME = "openai/gpt-oss-120b"  # Name of the LLM model to be used
EMBEDDING_MODEL_NAME = "jina-embeddings-v2-base-en"  # Name of the embedding model to be used

# CHUNKS / TEXT SPLITTING CONFIGURATION

CHUNK_SIZE = 1450  # Maximum number of characters in each chunk
CHUNK_OVERLAP = 70  # Number of characters to overlap between chunks

# Retrieval Configuration

TOP_K_RESULTS = 3  # Number of top results to retrieve from the vector store

# SYSTEM_INSTRUCTIONS

SYSTEM_PROMPT = (
    "You are an HR Policy Assistant. You will be provided with relevant information from the company's HR policy documents. "
    "Your task is to answer questions based on this information. If the information is not sufficient to answer the question, "
    "you should respond with 'I don't know'. Please provide clear and concise answers."
)

def check_api_keys() -> None:
    """Stop early with a clear message if a required API key is missing."""
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY. Please add it to your .env file.")
    if not JINA_API_KEY:
        raise ValueError("Missing JINA_API_KEY. Please add it to your .env file.")
    # if not QDRANT_URL or not QDRANT_API_KEY:
    #     raise ValueError("Missing QDRANT_URL/QDRANT_API_KEY. Please add them to your .env file.")
    # if not PORTKEY_API_KEY:
    #     raise ValueError("Missing PORTKEY_API_KEY. Please add it to your .env file.")


