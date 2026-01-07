"""
Project Dwight - Health Check Router
Provides health and status endpoints.
"""

from fastapi import APIRouter
from datetime import datetime

from config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns current status and basic system info.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - verifies all components are ready.
    """
    from core.rag_engine import is_rag_ready
    
    rag_status = await is_rag_ready()
    
    return {
        "ready": rag_status,
        "components": {
            "rag_engine": rag_status,
            "llm": True,  # Will be checked on first request
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - simple check that service is running.
    """
    return {"alive": True}
