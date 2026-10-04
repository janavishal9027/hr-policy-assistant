"""Wrap the retriever as a tool so that it can be used in the agent to search for relevant information based on the user query."""

from langchain.tools import tool
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def create_retriever_tool(retriever):
    """Return a @tool function that searches for relevant information based on the user query using the provided retriever."""

    @tool
    def create_search_tool(question: str) -> str:
        """Search for relevant information based on the user query using the provided retriever."""
        logger.info(f"Searching for information related to: {question}")
        results = retriever.invoke(question)
        return "\n\n".join([chunk.page_content for chunk in results])

    return create_search_tool