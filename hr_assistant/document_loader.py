"""Read the raw text file from the hr_policy directory."""


from langchain_community.document_loaders import TextLoader
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def load_documents(file_path: str = config.DATA_PATH):
    """Load a .txt file and return it as a list of Langchain Document objects."""
    logger.info(f"Loading documents from {file_path}")
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    logger.info("Loaded %d document(s)", len(documents))
    return documents