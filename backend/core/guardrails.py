"""
Project Dwight - Guardrails Module
Validates responses and enforces safety rules.
"""

from typing import List, Tuple
import re
import structlog

from core.intent_classifier import IntentType

logger = structlog.get_logger()

# Forbidden phrases that should never appear in responses
FORBIDDEN_PHRASES = [
    "i'm just a bot",
    "i'm just an ai",
    "as an ai",
    "as a language model",
    "i cannot access",
    "i don't have access to real-time",
    "i'm not sure, but",
    "based on my training",
    "based on my knowledge",
    "i think",
    "i believe",
    "probably",
    "maybe",
    "let me guess",
]

# Phrases that indicate hallucination risk
SPECULATION_INDICATORS = [
    "typically in the industry",
    "generally speaking",
    "in most cases",
    "usually companies",
    "standard practice is",
]

# Lead capture trigger keywords
LEAD_TRIGGER_KEYWORDS = [
    "quote", "quotation", "pricing", "price", "cost",
    "get started", "how do i start", "become a customer",
    "sign up", "onboard", "contact", "speak to someone",
    "interested in", "want to ship", "need shipping",
]

# Refusal template
REFUSAL_RESPONSE = "I don't have confirmed information on that at the moment. I can connect you with our team if you'd like."


async def validate_response(response: str, context: str) -> str:
    """
    Validate and clean the response.
    
    Args:
        response: Generated response from LLM
        context: The context that was provided
        
    Returns:
        Validated/cleaned response
    """
    validated = response
    
    # Check for forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in validated.lower():
            logger.warning("Forbidden phrase detected", phrase=phrase)
            validated = re.sub(
                re.escape(phrase),
                "",
                validated,
                flags=re.IGNORECASE
            )
    
    # Check for speculation without context backing
    if not context.strip():
        # If no context was provided, check for speculation
        for indicator in SPECULATION_INDICATORS:
            if indicator.lower() in validated.lower():
                logger.warning("Speculation detected without context")
                return REFUSAL_RESPONSE
    
    # Remove excessive apologies
    validated = re.sub(
        r"i('m| am) (so |very )?sorry,? (but |that )?",
        "",
        validated,
        flags=re.IGNORECASE
    )
    
    # Ensure response is not empty
    if not validated.strip():
        return REFUSAL_RESPONSE
    
    # Trim whitespace
    validated = validated.strip()
    
    return validated


async def check_lead_trigger(message: str, intent: IntentType) -> bool:
    """
    Check if the message should trigger a lead capture prompt.
    
    Args:
        message: User's message
        intent: Classified intent type
        
    Returns:
        True if lead capture should be triggered
    """
    # Sales intent always has potential for lead capture
    if intent == IntentType.SALES:
        return True
    
    # Check for lead trigger keywords
    message_lower = message.lower()
    for keyword in LEAD_TRIGGER_KEYWORDS:
        if keyword in message_lower:
            logger.info("Lead trigger detected", keyword=keyword)
            return True
    
    return False


async def check_response_quality(response: str, query: str) -> Tuple[bool, str]:
    """
    Check if response quality is acceptable.
    
    Args:
        response: Generated response
        query: Original user query
        
    Returns:
        Tuple of (is_acceptable, reason)
    """
    # Check minimum length
    if len(response) < 10:
        return False, "Response too short"
    
    # Check if response is just the refusal
    if response == REFUSAL_RESPONSE and len(query) < 20:
        # Short queries might legitimately get refusal
        return True, "OK"
    
    # Check for excessive repetition
    words = response.lower().split()
    if len(words) > 10:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            return False, "Excessive repetition detected"
    
    return True, "OK"


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: User input text
        
    Returns:
        Sanitized text
    """
    # Remove any potential prompt injection attempts
    injection_patterns = [
        r"ignore (?:all |previous |above )?instructions",
        r"forget (?:all |previous |above )?instructions",
        r"new instructions:",
        r"system prompt:",
        r"you are now",
        r"act as",
        r"pretend to be",
    ]
    
    sanitized = text
    for pattern in injection_patterns:
        if re.search(pattern, sanitized, re.IGNORECASE):
            logger.warning("Potential injection attempt detected", pattern=pattern)
            sanitized = re.sub(pattern, "[FILTERED]", sanitized, flags=re.IGNORECASE)
    
    # Limit length
    max_length = 2000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()
