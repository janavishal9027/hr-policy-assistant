"""
It identifies the policy guide before giving the answer it will try to understand the user intention.
"""

from hr_assistant.policy_dictionary import identify_policy
from hr_assistant.logger import get_logger

logger = get_logger(__name__)


def validate_policy_query(question: str):

    policies = identify_policy(question)

    logger.info(
        "Policy validation result: %s",
        policies
    )

    return {
        "policies": policies,
        "is_policy_query": bool(policies)
    }