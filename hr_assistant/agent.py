"""Build the agent that ties the llm and the search tool together to answer user queries based on the provided prompt and configuration."""

from langchain.agents import create_agent
from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def create_hr_assistant_agent(llm, tools):
    """Create an agent that ties the llm and the search tool together to answer user queries based on the provided prompt and configuration."""
    logger.info(f"Creating HR Assistant agent with LLM model: {config.LLM_MODEL_NAME} and tools: {[tool.name for tool in tools]}")
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=config.SYSTEM_PROMPT,
    )
    logger.info("HR Assistant agent created successfully.")
    return agent
