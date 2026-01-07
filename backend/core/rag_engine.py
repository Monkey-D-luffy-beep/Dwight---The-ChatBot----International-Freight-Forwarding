"""
Project Dwight - RAG Engine
Handles document retrieval and context building.
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import os
import pickle
import structlog
import faiss
import numpy as np

from config import settings
from core.embeddings import get_embedding, get_embeddings_batch
from core.intent_classifier import IntentType

logger = structlog.get_logger()

# Global variables for RAG state
_faiss_index: Optional[faiss.IndexFlatIP] = None
_documents: List[Dict[str, Any]] = []
_is_initialized: bool = False


async def initialize_rag_engine():
    """
    Initialize the RAG engine by loading or building the vector store.
    """
    global _faiss_index, _documents, _is_initialized
    
    vector_store_path = settings.vector_store_dir
    index_file = vector_store_path / "index.faiss"
    docs_file = vector_store_path / "documents.pkl"
    
    if index_file.exists() and docs_file.exists():
        # Load existing index
        logger.info("Loading existing FAISS index")
        _faiss_index = faiss.read_index(str(index_file))
        with open(docs_file, "rb") as f:
            _documents = pickle.load(f)
        logger.info("FAISS index loaded", num_documents=len(_documents))
    else:
        # Build new index
        logger.info("Building new FAISS index")
        await build_vector_store()
    
    _is_initialized = True


async def build_vector_store():
    """
    Build the vector store from source documents.
    """
    global _faiss_index, _documents
    
    # Load and chunk documents
    documents = await load_and_chunk_documents()
    
    if not documents:
        logger.warning("No documents found to index")
        _documents = []
        _faiss_index = faiss.IndexFlatIP(1536)  # OpenAI embedding dimension
        return
    
    # Generate embeddings
    logger.info("Generating embeddings", num_docs=len(documents))
    texts = [doc["content"] for doc in documents]
    
    # Process in batches to avoid rate limits
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = await get_embeddings_batch(batch)
        all_embeddings.extend(embeddings)
        logger.info("Processed batch", batch_num=i // batch_size + 1)
    
    # Create FAISS index
    embeddings_array = np.array(all_embeddings).astype('float32')
    faiss.normalize_L2(embeddings_array)
    
    dimension = embeddings_array.shape[1]
    _faiss_index = faiss.IndexFlatIP(dimension)
    _faiss_index.add(embeddings_array)
    
    _documents = documents
    
    # Save index
    vector_store_path = settings.vector_store_dir
    vector_store_path.mkdir(parents=True, exist_ok=True)
    
    faiss.write_index(_faiss_index, str(vector_store_path / "index.faiss"))
    with open(vector_store_path / "documents.pkl", "wb") as f:
        pickle.dump(_documents, f)
    
    logger.info("Vector store built and saved", num_documents=len(_documents))


async def load_and_chunk_documents() -> List[Dict[str, Any]]:
    """
    Load documents from data directory and split into chunks.
    """
    documents = []
    data_dir = settings.data_dir_path
    
    # Define bucket mappings
    bucket_intent_map = {
        "1_customer_support": IntentType.SUPPORT,
        "2_services_pricing": IntentType.SUPPORT,  # Can be both support and sales
        "3_sales_process": IntentType.SALES,
        "4_internal_policies": IntentType.INTERNAL,
    }
    
    for bucket_name, intent in bucket_intent_map.items():
        bucket_path = data_dir / bucket_name
        if not bucket_path.exists():
            continue
            
        for file_path in bucket_path.glob("*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                chunks = chunk_text(content, file_path.name)
                
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "content": chunk,
                        "source": file_path.name,
                        "bucket": bucket_name,
                        "intent": intent.value,
                        "chunk_index": i,
                    })
                    
                logger.debug("Processed file", file=file_path.name, chunks=len(chunks))
                
            except Exception as e:
                logger.error("Error processing file", file=str(file_path), error=str(e))
    
    logger.info("Documents loaded", total_chunks=len(documents))
    return documents


def chunk_text(text: str, source: str) -> List[str]:
    """
    Split text into chunks with overlap.
    
    Args:
        text: Full document text
        source: Source filename for context
        
    Returns:
        List of text chunks
    """
    chunk_size = settings.chunk_size
    overlap = settings.chunk_overlap
    
    # Split by sections (## headers in markdown)
    sections = text.split("\n## ")
    chunks = []
    
    for i, section in enumerate(sections):
        if i > 0:
            section = "## " + section
        
        # If section is small enough, keep as one chunk
        if len(section) <= chunk_size:
            chunks.append(section.strip())
        else:
            # Split large sections
            words = section.split()
            current_chunk = []
            current_length = 0
            
            for word in words:
                word_length = len(word) + 1
                if current_length + word_length > chunk_size and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    # Keep overlap words
                    overlap_words = int(overlap / 5)  # Approximate words for overlap
                    current_chunk = current_chunk[-overlap_words:] if overlap_words else []
                    current_length = sum(len(w) + 1 for w in current_chunk)
                
                current_chunk.append(word)
                current_length += word_length
            
            if current_chunk:
                chunks.append(" ".join(current_chunk))
    
    return [c for c in chunks if c.strip()]


async def retrieve_context(query: str, intent: IntentType, top_k: int = None) -> str:
    """
    Retrieve relevant context for a query.
    
    Args:
        query: User query
        intent: Classified intent type
        top_k: Number of results to return (default from settings)
        
    Returns:
        Combined context string from relevant documents
    """
    global _faiss_index, _documents
    
    if not _is_initialized or _faiss_index is None:
        logger.warning("RAG engine not initialized")
        return ""
    
    if _faiss_index.ntotal == 0:
        logger.warning("No documents in index")
        return ""
    
    top_k = top_k or settings.top_k_results
    
    # Generate query embedding
    query_embedding = await get_embedding(query)
    query_vector = np.array([query_embedding]).astype('float32')
    faiss.normalize_L2(query_vector)
    
    # Search
    scores, indices = _faiss_index.search(query_vector, min(top_k * 2, _faiss_index.ntotal))
    
    # Filter by intent and similarity threshold
    relevant_docs = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or score < settings.similarity_threshold:
            continue
            
        doc = _documents[idx]
        
        # Prioritize documents matching the intent, but include relevant ones from other buckets
        intent_match = doc["intent"] == intent.value
        
        relevant_docs.append({
            "content": doc["content"],
            "source": doc["source"],
            "score": float(score),
            "intent_match": intent_match
        })
    
    # Sort by intent match first, then by score
    relevant_docs.sort(key=lambda x: (x["intent_match"], x["score"]), reverse=True)
    
    # Take top_k results
    top_docs = relevant_docs[:top_k]
    
    if not top_docs:
        logger.info("No relevant documents found", query=query[:50])
        return ""
    
    # Combine context
    context_parts = []
    for doc in top_docs:
        context_parts.append(doc["content"])
    
    context = "\n\n---\n\n".join(context_parts)
    
    logger.info(
        "Context retrieved",
        num_docs=len(top_docs),
        avg_score=sum(d["score"] for d in top_docs) / len(top_docs)
    )
    
    return context


async def is_rag_ready() -> bool:
    """Check if RAG engine is ready."""
    return _is_initialized and _faiss_index is not None
