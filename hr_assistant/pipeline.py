"""
Wire all components together to form a pipeline. This is the main entry point for the HR Assistant application.

This is the single entry point that main.py (CLI) and app.py (Streamlit) both call to run the HR Assistant application. 
It orchestrates the entire process, from loading the HR policy documents, creating embeddings, storing them in a vector store, and setting up the agent to answer user queries.
"""

import time

from hr_assistant import config
from hr_assistant.document_loader import load_documents
from hr_assistant.llm import get_llm_response
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
from langchain_core.messages import AIMessageChunk

logger = get_logger(__name__)

# ============================================================
# BUILD VECTOR STORE
# ============================================================

def build_vector_store_for_document(
    file_path: str = config.DATA_PATH
):
    """
    Load + split + embed the document.

    Reuses an existing saved vector store if one is available.
    """

    if vector_store_exists():

        print(
            "Found a saved vector store on disk, "
            "(loading it...) - fast, no re-embedding needed."
        )

        logger.info(
            "Vector store already exists on disk, "
            "loading and reusing it..."
        )

        return load_vector_store()

    print(
        "No saved vector store found on disk, "
        "(building it...) - this may take a while."
    )

    logger.info(
        "No saved vector store found on disk, "
        "building a new one from scratch..."
    )

    # Load HR policy documents
    documents = load_documents(file_path)

    # Split documents into chunks
    chunks = split_text_into_chunks(documents)

    print(
        f"Loaded '{len(documents)}' documents and "
        f"split them into '{len(chunks)}' chunks."
    )

    # Build vector store
    vector_store = build_vector_store(chunks)

    # Save vector store
    save_vector_store(vector_store)

    print(
        f"Saved the vector store to "
        f"'{config.VECTOR_STORE_PATH}'."
    )

    return vector_store


# ============================================================
# BUILD HR ASSISTANT AGENT
# ============================================================



def build_hr_assistant_agent(
    file_path: str = config.DATA_PATH
):
    """
    Build the complete RAG Agent pipeline:

    Load
        ↓
    Split
        ↓
    Embed
        ↓
    Vector Store
        ↓
    Retriever
        ↓
    Search Tool
        ↓
    LLM
        ↓
    HR Assistant Agent
    """

    logger.info(
        "Starting to build the HR Assistant..."
    )

    # Check required API keys
    config.check_api_keys()

    # Check LangSmith tracing
    check_langsmith_tracing()

    # Build/load vector store
    vector_store = build_vector_store_for_document(
        file_path
    )

    # Create retriever
    retriever = get_retriever(vector_store)

    # Create retriever search tool
    search_tool = create_retriever_tool(
        retriever
    )

    # Create LLM
    llm = get_llm_response()

    # Create HR Assistant agent
    agent = create_hr_assistant_agent(
        llm,
        [search_tool]
    )

    logger.info(
        "HR Assistant built successfully. "
        "Now you can interact with it by asking questions."
    )

    return agent


# ============================================================
# NORMAL / NON-STREAMING ASK
# ============================================================

def ask(agent, question: str):
    """
    Ask a question to the HR Assistant agent and return
    the complete answer after the agent finishes processing.
    """

    logger.info(
        f"Asking the HR Assistant agent a question: {question}"
    )

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    answer = response["messages"][-1].content

    logger.info(
        f"Received answer from the HR Assistant agent: {answer}"
    )

    return answer

# ============================================================
# STREAMING ASK
# ============================================================

def ask_stream(agent, question: str):
    """
    Stream only the final AI response from the HR Assistant agent.

    Retriever/tool messages are ignored.

    The incoming LLM chunks are converted into word-level
    output for a smooth Streamlit experience.
    """

    logger.info(
        f"Asking the HR Assistant agent a question "
        f"(streaming): {question}"
    )

    buffer = ""

    try:

        for message_chunk, metadata in agent.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            stream_mode="messages",
        ):

            # ==================================================
            # ONLY AI MESSAGE CHUNKS
            # ==================================================

            if not isinstance(
                message_chunk,
                AIMessageChunk
            ):
                continue

            content = message_chunk.content

            if not content:
                continue

            # ==================================================
            # NORMAL STRING CONTENT
            # ==================================================

            if isinstance(content, str):

                buffer += content

            # ==================================================
            # CONTENT BLOCK FORMAT
            # ==================================================

            elif isinstance(content, list):

                for block in content:

                    if not isinstance(block, dict):
                        continue

                    text = block.get("text")

                    if text:
                        buffer += text

            else:

                continue

            # ==================================================
            # EXTRACT COMPLETE WORDS
            # ==================================================

            while " " in buffer:

                word, buffer = buffer.split(
                    " ",
                    1
                )

                if not word:
                    continue

                # Send word to Streamlit
                yield word + " "

                # Small UI delay for visible word-by-word effect
                time.sleep(0.03)

        # ======================================================
        # SEND REMAINING TEXT
        # ======================================================

        if buffer:

            yield buffer

    except Exception:

        logger.exception(
            "Error while streaming HR Assistant response."
        )

        raise