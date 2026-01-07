"""
Project Dwight - Configuration Module
Loads environment variables and provides configuration settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional
from pathlib import Path
import os

# Get the backend directory (where this config.py file lives)
BACKEND_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Project Dwight"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # LLM Provider (ollama or openai)
    llm_provider: str = "ollama"
    
    # Ollama Settings (local)
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "tinyllama"
    embedding_model: str = "nomic-embed-text"
    
    # LLM Parameters
    llm_temperature: float = 0.1
    llm_max_tokens: int = 500
    
    # OpenAI Settings (optional fallback)
    openai_api_key: Optional[str] = None
    
    # RAG Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    similarity_threshold: float = 0.5
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600  # 1 hour in seconds
    
    # CORS
    cors_origins: list = ["*"]
    
    # Google Sheets (Lead Capture)
    google_sheets_enabled: bool = False
    google_sheets_id: Optional[str] = None
    google_credentials_file: Optional[str] = None
    
    # Email Settings
    smtp_enabled: bool = False
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    notification_email: Optional[str] = None
    
    @property
    def data_dir_path(self) -> Path:
        """Get absolute path to data directory."""
        return PROJECT_ROOT / "data"
    
    @property
    def prompts_dir_path(self) -> Path:
        """Get absolute path to prompts directory."""
        return PROJECT_ROOT / ".claude"
    
    @property
    def vector_store_dir(self) -> Path:
        """Get absolute path to vector store directory."""
        return BACKEND_DIR / "data" / "processed" / "faiss_index"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra env variables not defined in Settings


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience access
settings = get_settings()
