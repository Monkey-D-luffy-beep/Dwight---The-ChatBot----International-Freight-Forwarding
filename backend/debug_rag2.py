import asyncio
import faiss
import pickle
import numpy as np
from pathlib import Path
from core.embeddings import get_embedding, _get_model
from config import settings

async def debug():
    # Load index
    vector_store_path = settings.vector_store_dir
    index_file = vector_store_path / "index.faiss"
    docs_file = vector_store_path / "documents.pkl"
    
    print(f"Loading from: {index_file}")
    index = faiss.read_index(str(index_file))
    with open(docs_file, "rb") as f:
        documents = pickle.load(f)
    
    print(f"Index has {index.ntotal} vectors")
    print(f"Index dimension: {index.d}")
    
    # Get embedding
    query = "What services do you offer?"
    print(f"\nGenerating embedding for: {query}")
    embedding = await get_embedding(query)
    print(f"Embedding dimension: {len(embedding)}")
    
    query_vector = np.array([embedding]).astype('float32')
    faiss.normalize_L2(query_vector)
    
    # Search
    scores, indices = index.search(query_vector, 5)
    
    print(f"\nRaw search results:")
    print(f"Similarity threshold: {settings.similarity_threshold}")
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx >= 0:
            doc = documents[idx]
            print(f"{i+1}. Score: {score:.4f} | {doc['source']} | {doc['content'][:80]}...")

if __name__ == "__main__":
    asyncio.run(debug())
