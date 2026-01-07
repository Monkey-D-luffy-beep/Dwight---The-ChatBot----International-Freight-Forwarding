# COPILOT SESSION STARTER - PROJECT DWIGHT

**USE THIS PROMPT EVERY TIME YOU START A NEW CODING SESSION**

Paste this into Copilot Chat to remind it of the project context:

---

## SESSION BRIEFING

I'm working on **Project Dwight**, an AI assistant for Tiger Logistics (international freight forwarding company).

**Key context:**
- Python + FastAPI backend
- RAG-based (FAISS + OpenAI embeddings)
- Three modes: Customer Support, Sales, Internal (auto-detected)
- Stateless (no chat history)
- Strict guardrails (context-only answering, explicit refusal when uncertain)
- Lead capture to Google Sheets + email
- Neutral, professional tone
- No databases, no authentication (MVP)

**Critical rules:**
1. Answer ONLY from provided context (RAG-constrained)
2. Refuse gracefully when context insufficient
3. Use type hints, docstrings, error handling
4. All secrets in environment variables
5. Structured logging (JSON)
6. Keep responses concise (2-4 sentences typically)

**Project structure:**
```
backend/
├── main.py
├── routers/chat.py, health.py
├── core/intent_classifier.py, rag_engine.py, llm_client.py, guardrails.py
├── services/lead_capture.py, logger.py
├── prompts/*.txt
└── data/raw_docs/, processed/
```

**Reference docs in `.claude/` folder:**
- `master_prompt.md` (bot behavior)
- `architecture_overview.md` (system design)
- `decisions.md` (why choices were made)

**Current task:** [DESCRIBE WHAT YOU'RE ABOUT TO BUILD]

Please generate code that follows the project standards and references the context above.

---

## QUICK REFERENCE FOR COMMON TASKS

### Task: Create FastAPI endpoint
**Pattern:**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class RequestModel(BaseModel):
    field: str

@router.post("/endpoint")
async def endpoint_name(request: RequestModel):
    try:
        # Logic here
        return {"result": "value"}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error message")
```

### Task: Load system prompt
**Pattern:**
```python
def load_prompt(mode: str) -> str:
    """Load system prompt for given mode."""
    prompt_file = f"prompts/system_{mode}.txt"
    with open(prompt_file, 'r') as f:
        return f.read()
```

### Task: RAG retrieval
**Pattern:**
```python
def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve relevant chunks from FAISS."""
    query_embedding = get_embedding(query)
    results = faiss_index.similarity_search(query_embedding, k=top_k)
    context = "\n\n".join([r.page_content for r in results])
    return context
```

### Task: Intent classification
**Pattern:**
```python
def classify_intent(query: str) -> str:
    """Classify query into support/sales/internal."""
    SALES_KW = ["quote", "pricing", "onboard", "get started"]
    INTERNAL_KW = ["policy", "procedure", "internal"]
    
    q = query.lower()
    if any(kw in q for kw in SALES_KW):
        return "sales"
    elif any(kw in q for kw in INTERNAL_KW):
        return "internal"
    return "support"
```

### Task: Guardrails check
**Pattern:**
```python
def validate_response(response: str, context: str) -> bool:
    """Check if response is appropriate."""
    # Check for refusal indicators
    if "don't have" in response.lower() and "information" in response.lower():
        return True
    
    # Check for hallucination indicators
    hallucination_phrases = [
        "based on my general knowledge",
        "typically in the industry",
        "from what I know"
    ]
    if any(phrase in response.lower() for phrase in hallucination_phrases):
        return False
    
    return True
```

### Task: Lead capture
**Pattern:**
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def capture_lead(email: str, phone: str, query: str) -> bool:
    """Save lead to Google Sheets and send email."""
    if not validate_email(email):
        return False
    
    # Append to Google Sheets
    # Send email notification
    
    return True
```

### Task: Error handling
**Pattern:**
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error("Error details", extra={"error": str(e), "query": query})
    return {"error": "User-friendly message", "error_code": "CODE"}
except Exception as e:
    logger.critical("Unexpected error", extra={"error": str(e)})
    return {"error": "Something went wrong. Please try again.", "error_code": "UNKNOWN"}
```

---

## TONE GUIDELINES FOR CODE COMMENTS

**Good comments:**
```python
# Classify intent using keyword matching (fast path)
# Fall back to LLM if ambiguous (slow path)
intent = classify_intent_keywords(query) or classify_intent_llm(query)
```

**Bad comments:**
```python
# This is a function that does classification
# It's really important and uses AI
```

**Docstring template:**
```python
def function_name(param: str) -> str:
    """
    Brief description of what function does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception occurs
    """
    pass
```

---

## DEBUGGING CHECKLIST

If Copilot-generated code doesn't work:

1. **Check imports** — Are all dependencies available?
2. **Check types** — Are type hints correct?
3. **Check paths** — Are file paths relative to project root?
4. **Check config** — Are environment variables loaded?
5. **Check logs** — Is structured logging working?
6. **Check errors** — Is error handling comprehensive?

---

## WHAT TO ASK COPILOT

**Good prompts:**
- "Generate the /chat endpoint following the project structure"
- "Create a FAISS ingestion script for documents in data/raw_docs/"
- "Write the intent classifier with keyword matching and LLM fallback"
- "Implement lead capture with Google Sheets API and email notification"

**Bad prompts:**
- "Make a chatbot" (too vague)
- "Add AI" (unclear)
- "Fix it" (no context)

---

## ENVIRONMENT VARIABLES REFERENCE

Create `.env` file with:
```
OPENAI_API_KEY=sk-...
GOOGLE_SHEETS_CREDENTIALS=...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SALES_EMAIL=sales@tigerlogistics.com
RATE_LIMIT_PER_HOUR=100
LOG_LEVEL=INFO
```

Load with:
```python
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

## QUALITY GATES BEFORE COMMITTING

- [ ] Type hints on all functions
- [ ] Docstrings on all public functions
- [ ] Error handling with try/except
- [ ] Logging at appropriate levels
- [ ] No hardcoded secrets
- [ ] No print statements (use logger)
- [ ] Code follows naming conventions
- [ ] Comments explain "why", not "what"

---

**Now tell me what you're building, and I'll generate code that fits this project perfectly.**