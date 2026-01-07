"""
Project Dwight - FastAPI Application Entry Point
Tiger Logistics AI Assistant Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from config import settings
from routers import chat, health
from core.rag_engine import initialize_rag_engine

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup
    logger.info("Starting Project Dwight", version=settings.app_version)
    
    # Initialize RAG engine
    try:
        await initialize_rag_engine()
        logger.info("RAG engine initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize RAG engine", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Project Dwight")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI Assistant for Tiger Logistics - Customer Support, Sales & Internal Knowledge",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])


@app.get("/")
async def root():
    """Root endpoint - basic info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "company": "Tiger Logistics"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
