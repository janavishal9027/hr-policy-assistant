"""Build the agent that ties the llm and the search tool together to answer user queries based on the provided prompt and configuration."""

from langchain.agents import create_agent
from hr_assistant import config

def create_hr_assistant_agent(llm, tools):
    """Create an agent that ties the llm and the search tool together to answer user queries based on the provided prompt and configuration."""
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=config.SYSTEM_PROMPT,
    )
