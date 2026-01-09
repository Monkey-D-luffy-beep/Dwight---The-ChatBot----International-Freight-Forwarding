"""
Project Dwight - Embeddings Module
Handles text embedding generation using sentence-transformers (local, no API needed).
"""

from typing import List
import numpy as np
import structlog
from sentence_transformers import SentenceTransformer

from config import settings

logger = structlog.get_logger()

# Lazy-loaded embedding model
_embedding_model = None


def _get_model():
    """Get or create the embedding model."""
    global _embedding_model
    if _embedding_model is None:
        logger.info("Loading embedding model", model=settings.embedding_model)
        _embedding_model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded successfully")
    return _embedding_model


async def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    try:
        model = _get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as e:
        logger.error("Embedding generation failed", error=str(e))
        raise


async def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batch.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    try:
        model = _get_model()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        logger.info("Batch embeddings generated", count=len(texts))
        return embeddings.tolist()
    except Exception as e:
        logger.error("Batch embedding generation failed", error=str(e))
        raise


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score (0 to 1)
    """
    a = np.array(vec1)
    b = np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
