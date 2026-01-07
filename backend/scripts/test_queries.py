"""
Project Dwight - Test Queries Script
Tests the RAG pipeline with sample queries.

Usage:
    python scripts/test_queries.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rag_engine import initialize_rag_engine, retrieve_context
from core.intent_classifier import classify_intent, IntentType
from core.llm_client import generate_response

# Test queries for each mode
TEST_QUERIES = {
    "support": [
        "What services does Tiger Logistics offer?",
        "How can I track my shipment?",
        "What documents do I need for customs clearance?",
        "What is the difference between FCL and LCL?",
        "Does Tiger Logistics handle air freight?",
    ],
    "sales": [
        "How much does shipping to Europe cost?",
        "How can I get a quote?",
        "How do I become a customer?",
        "What are your payment terms?",
        "I want to ship goods from Mumbai to London.",
    ],
    "internal": [
        "What is the escalation protocol?",
        "What are the quality standards?",
        "How do I handle customer complaints?",
    ],
    "edge_cases": [
        "Hello",
        "What is your CEO's phone number?",
        "Can you give me an exact price for shipping?",
        "What are your competitor's rates?",
    ]
}


async def test_single_query(query: str, expected_intent: str = None):
    """Test a single query through the pipeline."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print("-" * 60)
    
    # Classify intent
    intent = await classify_intent(query)
    print(f"Intent: {intent.value}")
    
    if expected_intent:
        match = "✅" if intent.value == expected_intent else "❌"
        print(f"Expected: {expected_intent} {match}")
    
    # Retrieve context
    context = await retrieve_context(query, intent)
    context_preview = context[:200] + "..." if len(context) > 200 else context
    print(f"Context ({len(context)} chars): {context_preview}")
    
    # Generate response
    response = await generate_response(query, context, intent)
    print(f"\nResponse:\n{response}")
    
    return {
        "query": query,
        "intent": intent.value,
        "context_length": len(context),
        "response": response
    }


async def main():
    """Run all test queries."""
    print("=" * 60)
    print("Project Dwight - Query Testing")
    print("=" * 60)
    
    # Initialize RAG
    print("\nInitializing RAG engine...")
    await initialize_rag_engine()
    print("RAG engine ready!")
    
    results = []
    
    # Test support queries
    print("\n" + "=" * 60)
    print("SUPPORT MODE TESTS")
    print("=" * 60)
    for query in TEST_QUERIES["support"]:
        result = await test_single_query(query, "support")
        results.append(result)
    
    # Test sales queries
    print("\n" + "=" * 60)
    print("SALES MODE TESTS")
    print("=" * 60)
    for query in TEST_QUERIES["sales"]:
        result = await test_single_query(query, "sales")
        results.append(result)
    
    # Test internal queries
    print("\n" + "=" * 60)
    print("INTERNAL MODE TESTS")
    print("=" * 60)
    for query in TEST_QUERIES["internal"]:
        result = await test_single_query(query, "internal")
        results.append(result)
    
    # Test edge cases
    print("\n" + "=" * 60)
    print("EDGE CASE TESTS")
    print("=" * 60)
    for query in TEST_QUERIES["edge_cases"]:
        result = await test_single_query(query)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total queries tested: {len(results)}")
    
    # Calculate stats
    avg_context = sum(r["context_length"] for r in results) / len(results)
    avg_response = sum(len(r["response"]) for r in results) / len(results)
    
    print(f"Average context length: {avg_context:.0f} chars")
    print(f"Average response length: {avg_response:.0f} chars")
    
    # Intent distribution
    intent_counts = {}
    for r in results:
        intent_counts[r["intent"]] = intent_counts.get(r["intent"], 0) + 1
    print(f"Intent distribution: {intent_counts}")
    
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    asyncio.run(main())
