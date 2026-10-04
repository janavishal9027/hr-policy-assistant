"""LangSmith tracing configuration for LangChain.

This module sets up the tracing configuration for LangChain using environment variables. It allows you to enable or disable tracing, specify the endpoint, API key, and project name for LangSmith tracing.

It is important to note that this configuration is optional and can be customized based on our requirements. 

If tracing is not needed, you can set the LANGSMITH_TRACING environment variable to "false" or leave it unset.

The tracing configuration is used to monitor and analyze the behavior of LangChain applications, providing insights into their performance and usage patterns. 

It can be helpful for debugging, optimization, and understanding how the application interacts with LangChain components.

"""


from hr_assistant import config
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def check_langsmith_tracing() -> None:
    """Check if LangSmith tracing is enabled and log the configuration details."""

    tracing_on = config.LANGSMITH_TRACING.lower() == "true"

    if tracing_on and config.LANGSMITH_API_KEY:
        logger.info(
            "LangSmith tracing is ENABLED - project: %s, traces at %s",
            config.LANGSMITH_PROJECT,
            config.LANGSMITH_ENDPOINT,
        )
    else:
        logger.info("LangSmith tracing is disabled.")