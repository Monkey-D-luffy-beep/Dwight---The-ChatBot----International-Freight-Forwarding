"""Debug RAG retrieval"""
import sys
sys.path.insert(0, 'c:/Users/SauravPayal/project/Dwight/backend')

import asyncio
import numpy as np
import faiss
from core.embeddings import get_embedding
from config import settings
import pickle

async def test():
    # Load index
    vector_store_path = settings.vector_store_dir
    index = faiss.read_index(str(vector_store_path / 'index.faiss'))
    with open(vector_store_path / 'documents.pkl', 'rb') as f:
        docs = pickle.load(f)
    
    print(f'Index has {index.ntotal} vectors')
    print(f'Loaded {len(docs)} documents')
    print(f'Similarity threshold: {settings.similarity_threshold}')
    
    # Get query embedding
    query = 'What services does Tiger Logistics offer?'
    emb = await get_embedding(query)
    query_vec = np.array([emb]).astype('float32')
    faiss.normalize_L2(query_vec)
    
    # Search without threshold
    scores, indices = index.search(query_vec, 5)
    print(f'\nTop 5 results for: "{query}"')
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        source = docs[idx]["source"]
        content = docs[idx]["content"][:150].replace('\n', ' ')
        print(f'{i+1}. Score: {score:.4f} | {source}')
        print(f'   {content}...')
        print()

asyncio.run(test())
