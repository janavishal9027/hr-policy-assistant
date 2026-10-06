"""
Agentic harness for the HR Policy Assistant.

The harness sits between the application pipeline/UI and the
LangChain agent.

Responsibilities:
    1. Classify the user's HR policy query.
    2. Invoke the underlying agent normally.
    3. Stream the underlying agent response.
"""

from hr_assistant.policy_guard import validate_policy_query
from hr_assistant.logger import get_logger

logger = get_logger(__name__)


class HRAgentHarness:

    def __init__(self, agent):
        self.agent = agent

    # ============================================================
    # POLICY / INTENT CLASSIFICATION
    # ============================================================

    def classify(self, question: str):
        """
        Identify the likely HR policy category before
        sending the question to the agent.
        """

        classification = validate_policy_query(question)

        logger.info(
            "Agentic harness classification: %s",
            classification
        )

        return classification

    # ============================================================
    # NORMAL INVOCATION
    # ============================================================

    def invoke(self, input_data):
        """
        Execute the underlying LangChain agent normally.

        This keeps the same interface as the original agent.
        """

        logger.info("Invoking HR Assistant agent.")

        return self.agent.invoke(input_data)

    # ============================================================
    # STREAMING
    # ============================================================

    def stream(self, input_data):
        """
        Stream messages from the underlying LangChain agent.

        The application should NOT need to know about LangChain's
        stream_mode configuration.
        """

        # --------------------------------------------------------
        # Extract user question
        # --------------------------------------------------------

        messages = input_data.get("messages", [])

        question = ""

        if messages:

            last_message = messages[-1]

            if isinstance(last_message, dict):
                question = last_message.get(
                    "content",
                    ""
                )

            else:
                question = getattr(
                    last_message,
                    "content",
                    ""
                )

        logger.info(
            "Starting agentic streaming for question: %s",
            question
        )

        # --------------------------------------------------------
        # Classify before agent execution
        # --------------------------------------------------------

        classification = self.classify(question)

        logger.info(
            "Policy classification before streaming: %s",
            classification
        )

        # --------------------------------------------------------
        # Stream underlying LangChain agent
        # --------------------------------------------------------

        for message_chunk, metadata in self.agent.stream(
            input_data,
            stream_mode="messages",
        ):

            yield message_chunk, metadata