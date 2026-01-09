import asyncio
from core.rag_engine import initialize_rag_engine, retrieve_context
from core.intent_classifier import IntentType

async def test():
    print("Initializing RAG...")
    await initialize_rag_engine()
    print("RAG initialized!")
    
    print("\nTesting retrieve_context...")
    context = await retrieve_context('What services do you offer?', IntentType.SUPPORT)
    print(f'Context length: {len(context)}')
    if context:
        print(f'Context preview: {context[:500]}...')
    else:
        print('CONTEXT IS EMPTY!')

if __name__ == "__main__":
    asyncio.run(test())
