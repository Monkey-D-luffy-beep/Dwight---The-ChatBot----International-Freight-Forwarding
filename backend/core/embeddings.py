"""
Project Dwight - Embeddings Module
Handles text embedding generation using Ollama (local).
"""

from typing import List
import numpy as np
import ollama
import structlog

from config import settings

logger = structlog.get_logger()


async def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text using Ollama.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    try:
        response = ollama.embeddings(
            model=settings.embedding_model,
            prompt=text
        )
        return response['embedding']
    except Exception as e:
        logger.error("Embedding generation failed", error=str(e))
        raise


async def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batch using Ollama.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    embeddings = []
    try:
        for i, text in enumerate(texts):
            response = ollama.embeddings(
                model=settings.embedding_model,
                prompt=text
            )
            embeddings.append(response['embedding'])
            
            # Log progress every 20 texts
            if (i + 1) % 20 == 0:
                logger.debug("Embedding progress", completed=i+1, total=len(texts))
        
        return embeddings
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
