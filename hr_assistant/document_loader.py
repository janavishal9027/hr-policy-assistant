"""Read the raw text file from the hr_policy directory."""


from langchain_community.document_loaders import TextLoader
from hr_assistant import config

def load_documents(file_path: str = config.DATA_PATH):
    """Load a .txt file and return it as a list of Langchain Document objects."""
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    return documents 