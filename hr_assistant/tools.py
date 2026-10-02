"""Wrap the retriever as a tool so that it can be used in the agent to search for relevant information based on the user query."""

from langchain.tools import tool

def create_retriever_tool(retriever):
    """Return a @tool function that searches for relevant information based on the user query using the provided retriever."""

    @tool
    def create_search_tool(question: str) -> str:
        """Search for relevant information based on the user query using the provided retriever."""
        results = retriever.invoke(question)
        return "\n\n".join([chunk.page_content for chunk in results])

    return create_search_tool