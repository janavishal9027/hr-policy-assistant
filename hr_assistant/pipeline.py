"""
Wire all components together to form a pipeline. This is the main entry point for the HR Assistant application.

This is the single entry point that main.py (CLI) and app.py (Streamlit) both call to run the HR Assistant application. 
It orchestrates the entire process, from loading the HR policy documents, creating embeddings, storing them in a vector store, and setting up the agent to answer user queries.
"""

from hr_assistant import config
from hr_assistant.document_loader import load_documents
from hr_assistant.llm import get_llm_response
from hr_assistant.embeddings import get_embedding_model
from hr_assistant.splitter import split_text_into_chunks
from hr_assistant.tools import create_retriever_tool
from hr_assistant.agent import create_hr_assistant_agent
from hr_assistant.vector_store import (
    build_vector_store,
    save_vector_store,
    load_vector_store,
    vector_store_exists,
    get_retriever
)
from hr_assistant.logger import get_logger
from hr_assistant.tracing import check_langsmith_tracing

logger = get_logger(__name__)

# Building vector store

def build_vector_store_for_document(file_path: str = config.DATA_PATH):
    """Load + split + embed the document, reusing a saved index if it exists, and return the vector store."""
    if vector_store_exists():
        print("Found a saved vector store on disk, (loading it...) - fast, no re-embedding needed.")
        logger.info("Vector store already exists on disk, loading and reusing it...")
        return load_vector_store()

    print("No saved vector store found on disk, (building it...) - this may take a while.")
    logger.info("No saved vector store found on disk, building a new one from scratch...")
    documents = load_documents(file_path)  # Load the HR policy documents
    chunks = split_text_into_chunks(documents)  # Split the documents into chunks
    print(f"Loaded '{len(documents)}' documents and split them into '{len(chunks)}' chunks.")

    vector_store = build_vector_store(chunks)  # Build the vector store from the chunks
    save_vector_store(vector_store)  # Save the vector store to disk
    print(f"Saved the vector store to '{config.VECTOR_STORE_PATH}'.")
    return vector_store  # Return the vector store


# Building the agent

def build_hr_assistant_agent(file_path: str = config.DATA_PATH):
    """ Build the full RAG Agent pipeline: Load + Split + Embed + Store + Retrieve + Answer. """
    logger.info("Starting to build the HR Assistant...")
    config.check_api_keys()  # Check if the required API keys are present
    check_langsmith_tracing()  # Check if LangSmith tracing is enabled

    vector_store = build_vector_store_for_document(file_path)  # Build the vector store for the document
    retriever = get_retriever(vector_store)  # Get a retriever from the vector store
    search_tool = create_retriever_tool(retriever)  # Create a search tool using the retriever

    llm = get_llm_response()  # Get the LLM response
    agent = create_hr_assistant_agent(llm, [search_tool])  # Create the HR Assistant agent using the LLM and search tool

    logger.info("HR Assistant built successfully. Now you can interact with it by asking questions.")
    return agent  # Return the HR Assistant agent


# Last invocation of the pipeline to build the agent, which is called by main.py and app.py

def ask(agent, question: str):
    """Ask a question to the HR Assistant agent and return the answer."""
    logger.info(f"Asking the HR Assistant agent a question: {question}")
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )  # Invoke the agent with the user question
    answer = response["messages"][-1].content  # Return the content of the response
    logger.info(f"Received answer from the HR Assistant agent: {answer}")
    return answer