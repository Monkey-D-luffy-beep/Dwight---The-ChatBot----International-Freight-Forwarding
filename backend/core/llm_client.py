"""
Project Dwight - LLM Client
Handles interactions with the language model using Ollama (local).
"""

from typing import Optional
from pathlib import Path
import ollama
import structlog

from config import settings
from core.intent_classifier import IntentType

logger = structlog.get_logger()

# Cache for loaded prompts
_prompt_cache: dict = {}


def load_system_prompt(intent: IntentType) -> str:
    """
    Load the appropriate system prompt for the given intent.
    
    Args:
        intent: The classified intent type
        
    Returns:
        System prompt string
    """
    prompt_files = {
        IntentType.SUPPORT: "system_support.txt",
        IntentType.SALES: "system_sales.txt",
        IntentType.INTERNAL: "system_internal.txt",
    }
    
    filename = prompt_files.get(intent, "system_support.txt")
    
    # Check cache
    if filename in _prompt_cache:
        return _prompt_cache[filename]
    
    # Try multiple paths
    possible_paths = [
        settings.prompts_dir_path / filename,
        Path("../.claude") / filename,
        Path(".claude") / filename,
    ]
    
    for path in possible_paths:
        if path.exists():
            content = path.read_text(encoding="utf-8")
            _prompt_cache[filename] = content
            logger.debug("Loaded prompt", file=str(path))
            return content
    
    # Fallback default prompt
    logger.warning("Prompt file not found, using default", filename=filename)
    return get_default_prompt(intent)


def get_default_prompt(intent: IntentType) -> str:
    """Get a default prompt if file not found."""
    base = """You are a helpful assistant for Tiger Logistics, an international freight forwarding company.

CORE RULES:
1. Answer ONLY using the provided context below
2. If the answer is not in the context, say: "I don't have confirmed information on that at the moment. I can connect you with our team if you'd like."
3. Never guess or make up information
4. Be concise, professional, and helpful

CONTEXT WILL BE PROVIDED BELOW:
---
{context}
---

USER QUERY:
{query}

Provide a helpful, accurate response based strictly on the context above."""
    
    return base


async def generate_response(
    query: str,
    context: str,
    intent: IntentType,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Generate a response using the LLM.
    
    Args:
        query: User's question
        context: Retrieved context from RAG
        intent: Classified intent type
        temperature: Optional override for temperature
        max_tokens: Optional override for max tokens
        
    Returns:
        Generated response string
    """
    try:
        # Load appropriate system prompt
        system_prompt = load_system_prompt(intent)
        
        # Format the prompt with context and query
        formatted_prompt = system_prompt.replace("{context}", context).replace("{query}", query)
        
        # Handle empty context
        if not context.strip():
            formatted_prompt = system_prompt.replace(
                "{context}",
                "[No relevant context found in knowledge base]"
            ).replace("{query}", query)
        
        # Generate response using Ollama
        response = ollama.chat(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": formatted_prompt},
                {"role": "user", "content": query}
            ],
            options={
                "temperature": temperature or settings.llm_temperature,
                "num_predict": max_tokens or settings.llm_max_tokens,
            }
        )
        
        generated_text = response['message']['content'].strip()
        
        logger.info(
            "Response generated",
            model=settings.llm_model,
            eval_count=response.get('eval_count', None)
        )
        
        return generated_text
        
    except Exception as e:
        logger.error("LLM generation failed", error=str(e))
        return "I'm having trouble processing your request right now. Please try again or contact us at info@tigerlogistics.in for assistance."
