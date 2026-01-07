"""
Project Dwight - Document Ingestion Script
Processes documents and builds the FAISS vector store.

Usage:
    python scripts/ingest_documents.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from core.rag_engine import build_vector_store, load_and_chunk_documents


async def main():
    """Main ingestion function."""
    print("=" * 50)
    print("Project Dwight - Document Ingestion")
    print("=" * 50)
    
    # Check data directory
    data_dir = settings.data_dir_path
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        print("Please ensure your documents are in the data/ directory")
        return
    
    # List available documents
    print("\nScanning data directory...")
    total_files = 0
    for bucket in ["1_customer_support", "2_services_pricing", "3_sales_process", "4_internal_policies"]:
        bucket_path = data_dir / bucket
        if bucket_path.exists():
            files = list(bucket_path.glob("*.md"))
            print(f"  {bucket}: {len(files)} files")
            for f in files:
                print(f"    - {f.name}")
            total_files += len(files)
    
    if total_files == 0:
        print("\nNo documents found. Please add .md files to the data buckets.")
        return
    
    print(f"\nTotal files found: {total_files}")
    
    # Load and chunk documents
    print("\nLoading and chunking documents...")
    documents = await load_and_chunk_documents()
    print(f"Created {len(documents)} chunks")
    
    # Build vector store
    print("\nBuilding vector store (this may take a moment)...")
    await build_vector_store()
    
    # Verify
    vector_store_path = settings.vector_store_dir
    if (vector_store_path / "index.faiss").exists():
        print(f"\n✅ Vector store created successfully!")
        print(f"   Location: {vector_store_path}")
    else:
        print("\n❌ Failed to create vector store")
        return
    
    print("\n" + "=" * 50)
    print("Ingestion complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
