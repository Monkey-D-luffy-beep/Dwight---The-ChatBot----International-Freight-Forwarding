"""
Project Dwight - Intent Classifier
Automatically detects user intent to route to appropriate mode.
"""

from enum import Enum
from typing import List, Tuple
import re
import structlog

logger = structlog.get_logger()


class IntentType(Enum):
    """Types of user intents."""
    SUPPORT = "support"      # Customer support queries
    SALES = "sales"          # Sales/lead qualification queries
    INTERNAL = "internal"    # Internal knowledge queries


# Keywords and patterns for intent classification
SALES_KEYWORDS = [
    "price", "pricing", "cost", "quote", "quotation", "rate", "rates",
    "how much", "charges", "fee", "fees", "budget",
    "get started", "become a customer", "onboard", "onboarding",
    "sign up", "signup", "register", "contract", "agreement",
    "payment terms", "credit", "partner", "partnership",
    "interested in", "want to use", "looking for", "need shipping"
]

SALES_PATTERNS = [
    r"how (?:much|do i|can i|to) (?:pay|start|begin|sign)",
    r"(?:can you|could you) (?:give|send|provide) (?:me )?(?:a )?quote",
    r"what (?:are|is) (?:the|your) (?:price|cost|rate|charge)",
    r"i (?:want|need|am looking) to (?:ship|send|export|import)",
    r"(?:pricing|quote|cost) for",
]

INTERNAL_KEYWORDS = [
    "policy", "policies", "procedure", "procedures", "protocol",
    "escalation", "escalate", "sla", "kpi", "standard",
    "internal", "employee", "staff", "team", "department",
    "quality standard", "compliance", "audit"
]

INTERNAL_PATTERNS = [
    r"what is (?:the|our) (?:policy|procedure|protocol)",
    r"how (?:do|should) (?:we|i|staff) (?:handle|process|escalate)",
    r"(?:internal|staff|employee) (?:guide|guideline|policy)",
]


def _calculate_keyword_score(text: str, keywords: List[str]) -> float:
    """Calculate how many keywords match in the text."""
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword in text_lower)
    return matches / len(keywords) if keywords else 0


def _check_patterns(text: str, patterns: List[str]) -> bool:
    """Check if any pattern matches the text."""
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)


async def classify_intent(message: str) -> IntentType:
    """
    Classify user intent based on message content.
    
    Args:
        message: User's message text
        
    Returns:
        IntentType indicating support, sales, or internal mode
    """
    message_lower = message.lower()
    
    # Check for sales intent
    sales_keyword_score = _calculate_keyword_score(message, SALES_KEYWORDS)
    sales_pattern_match = _check_patterns(message, SALES_PATTERNS)
    
    if sales_pattern_match or sales_keyword_score > 0.05:
        logger.debug("Classified as SALES", score=sales_keyword_score)
        return IntentType.SALES
    
    # Check for internal intent
    internal_keyword_score = _calculate_keyword_score(message, INTERNAL_KEYWORDS)
    internal_pattern_match = _check_patterns(message, INTERNAL_PATTERNS)
    
    if internal_pattern_match or internal_keyword_score > 0.05:
        logger.debug("Classified as INTERNAL", score=internal_keyword_score)
        return IntentType.INTERNAL
    
    # Default to support
    logger.debug("Classified as SUPPORT (default)")
    return IntentType.SUPPORT


async def get_intent_context(intent: IntentType) -> str:
    """
    Get the appropriate system prompt file path for the intent.
    
    Args:
        intent: The classified intent type
        
    Returns:
        Path to the system prompt file
    """
    prompt_map = {
        IntentType.SUPPORT: "prompts/system_support.txt",
        IntentType.SALES: "prompts/system_sales.txt",
        IntentType.INTERNAL: "prompts/system_internal.txt",
    }
    return prompt_map.get(intent, "prompts/system_support.txt")
