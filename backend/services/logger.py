"""
Project Dwight - Logging Service
Structured logging for chat interactions.
"""

from datetime import datetime
from typing import Optional
import json
import structlog

logger = structlog.get_logger()


async def log_chat_interaction(
    session_id: str,
    message: str,
    response: str,
    intent: str,
    duration_ms: float,
    context_length: Optional[int] = None,
    tokens_used: Optional[int] = None
):
    """
    Log a chat interaction for analytics and debugging.
    
    Args:
        session_id: User session identifier
        message: User's message
        response: Generated response
        intent: Classified intent type
        duration_ms: Response time in milliseconds
        context_length: Length of retrieved context
        tokens_used: LLM tokens used
    """
    logger.info(
        "chat_interaction",
        session_id=session_id,
        message_length=len(message),
        response_length=len(response),
        intent=intent,
        duration_ms=round(duration_ms, 2),
        context_length=context_length,
        tokens_used=tokens_used,
        timestamp=datetime.utcnow().isoformat()
    )


async def log_error(
    error_type: str,
    error_message: str,
    session_id: Optional[str] = None,
    context: Optional[dict] = None
):
    """
    Log an error with context.
    
    Args:
        error_type: Type/category of error
        error_message: Error description
        session_id: Optional session identifier
        context: Additional context as dict
    """
    logger.error(
        "error",
        error_type=error_type,
        error_message=error_message,
        session_id=session_id,
        context=context,
        timestamp=datetime.utcnow().isoformat()
    )


async def log_lead_capture(
    session_id: str,
    email_domain: str,
    success: bool
):
    """
    Log a lead capture event.
    
    Args:
        session_id: User session identifier
        email_domain: Domain of email (for analytics without PII)
        success: Whether capture was successful
    """
    logger.info(
        "lead_capture",
        session_id=session_id,
        email_domain=email_domain,
        success=success,
        timestamp=datetime.utcnow().isoformat()
    )


async def log_rag_retrieval(
    query: str,
    num_results: int,
    avg_score: float,
    intent: str
):
    """
    Log RAG retrieval metrics.
    
    Args:
        query: Search query
        num_results: Number of results returned
        avg_score: Average similarity score
        intent: Query intent
    """
    logger.info(
        "rag_retrieval",
        query_length=len(query),
        num_results=num_results,
        avg_score=round(avg_score, 4),
        intent=intent,
        timestamp=datetime.utcnow().isoformat()
    )
