# COPILOT MASTER CONTEXT - PROJECT DWIGHT
## Tiger Logistics AI Assistant

**PURPOSE:** This document establishes the complete context for GitHub Copilot to assist with Project Dwight development.

---

## PROJECT OVERVIEW

**Project Name:** Dwight  
**Company:** Tiger Logistics (International Freight Forwarding)  
**Goal:** Build a unified AI assistant that handles customer support, lead qualification, and internal knowledge queries using RAG (Retrieval-Augmented Generation).

**Core Principle:** Trust over coverage. Better to say "I don't know" than to hallucinate.

---

## TECHNICAL STACK

**Backend:**
- Python 3.11+
- FastAPI
- LangChain (lightweight usage)
- FAISS (local vector store)
- OpenAI GPT-4o-mini
- Google Sheets API (lead capture)
- SMTP (email notifications)

**Frontend:**
- Plain HTML + CSS + JavaScript
- Embeddable chat widget
- No frameworks (React/Vue) for MVP

**Infrastructure:**
- Backend: Railway or Render
- Frontend: Netlify or Vercel
- No database (stateless)
- Environment variables for secrets

---

## PROJECT STRUCTURE

```
project_dwight/
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Environment config
│   ├── requirements.txt
│   │
│   ├── routers/
│   │   ├── chat.py                # /chat endpoint
│   │   └── health.py              # /health endpoint
│   │
│   ├── core/
│   │   ├── intent_classifier.py  # Detect mode (support/sales/internal)
│   │   ├── rag_engine.py         # Document retrieval
│   │   ├── embeddings.py         # Vector generation & search
│   │   ├── llm_client.py         # OpenAI wrapper
│   │   └── guardrails.py         # Response validation
│   │
│   ├── services/
│   │   ├── lead_capture.py       # Google Sheets + email
│   │   └── logger.py             # Structured logging
│   │
│   ├── prompts/
│   │   ├── system_support.txt
│   │   ├── system_sales.txt
│   │   ├── system_internal.txt
│   │   └── refusal_template.txt
│   │
│   ├── data/
│   │   ├── raw_docs/
│   │   └── processed/
│   │
│   └── scripts/
│       ├── ingest_documents.py   # Convert docs → embeddings
│       └── test_queries.py
│
├── frontend/
│   ├── widget.js
│   ├── widget.css
│   └── index.html
│
└── .claude/                       # Project docs
    ├── master_prompt.md
    ├── progress.md
    ├── decisions.md
    ├── document_ingestion_guide.md
    ├── architecture_overview.md
    ├── system_support.txt
    ├── system_sales.txt
    ├── system_internal.txt
    └── refusal_template.txt
```

---

## ARCHITECTURE PRINCIPLES

### 1. **Three Operating Modes (Automatic Detection)**
- **Customer Support:** FAQs, processes, documentation
- **Sales/Lead Qualification:** Quotes, onboarding, buying intent
- **Internal Knowledge:** Policies, procedures, staff guidance

Intent is detected automatically. User never chooses mode.

### 2. **RAG-Constrained Answering**
- Bot ONLY answers from provided context
- No general knowledge usage
- No guessing or speculation
- Strict refusal when context insufficient

### 3. **Guardrails (Non-Negotiable)**
- Temperature: 0.0-0.2 (low variability)
- Context-only responses
- Explicit "I don't know" when uncertain
- Never make pricing/timeline promises unless in context
- Always offer escalation to human

### 4. **Lead Capture Logic**
Proactive contact request ONLY if:
- User asks about pricing/quotes
- User asks how to proceed/get started
- User explicitly requests human contact

Exact phrasing:
```
"To assist you further, I can connect you with our team.
Please share your email address and phone number, and a representative will reach out."
```

### 5. **No Chat History**
- Stateless system (no memory between sessions)
- Simpler architecture
- No privacy concerns
- Lower cost

---

## CODE QUALITY STANDARDS

### General Rules
- Type hints for all functions
- Docstrings for all public functions
- Error handling with try/except
- Structured logging (JSON format)
- No hardcoded values (use config.py)

### Naming Conventions
- Files: `snake_case.py`
- Functions: `snake_case()`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Variables: `snake_case`

### Security Requirements
- All secrets in environment variables
- Input validation on all endpoints
- Rate limiting (100 req/hour per IP)
- No PII in logs
- CORS properly configured

### Performance
- Response time target: <2 seconds
- Async operations where possible
- Connection pooling for API calls
- Efficient FAISS queries (top-k=3-5)

---

## CRITICAL CONSTRAINTS

### ❌ NEVER:
- Use external databases (PostgreSQL, MongoDB, etc.)
- Store chat history persistently
- Use localStorage or sessionStorage in frontend
- Make API calls to unverified sources
- Guess or speculate when context missing
- Use aggressive marketing language
- Make promises about pricing/timelines unless in context
- Show sources to user (logged internally only)

### ✅ ALWAYS:
- Validate inputs before processing
- Use structured logging
- Handle errors gracefully
- Provide escalation path
- Keep responses concise (2-4 sentences typically)
- Use neutral, professional tone
- Follow the master prompt rules strictly

---

## TONE & LANGUAGE RULES

**Tone:** Neutral, professional, clear, concise

**Avoid:**
- Emojis
- Exclamation marks (use sparingly)
- Marketing fluff ("amazing", "incredible", "best")
- Absolutes ("always", "never", "guaranteed")
- Self-referential statements ("As an AI...")
- Over-apologizing

**Prefer:**
- Direct, helpful statements
- Bullet points for lists
- Short paragraphs (2-3 sentences)
- Neutral qualifiers ("typically", "generally", "as per standard process")

---

## API DESIGN

### POST /chat
**Request:**
```json
{
  "query": "string",
  "session_id": "optional-string"
}
```

**Response:**
```json
{
  "response": "string",
  "intent": "support|sales|internal",
  "lead_captured": boolean,
  "metadata": {
    "tokens_used": number,
    "confidence": number
  }
}
```

### GET /health
**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "ISO-8601"
}
```

---

## RAG IMPLEMENTATION DETAILS

### Document Processing
1. Chunk size: 500-1000 characters
2. Overlap: 100 characters
3. Embedding model: `text-embedding-3-small` (OpenAI)
4. Vector store: FAISS (local)

### Retrieval
1. Query → embedding
2. Similarity search (cosine)
3. Top-k: 3-5 chunks
4. Concatenate as context
5. Pass to LLM with system prompt

### Context Injection
```python
context = "\n\n".join([chunk.content for chunk in retrieved_chunks])

system_prompt = load_prompt(intent_mode)  # support/sales/internal
final_prompt = system_prompt.format(context=context, query=user_query)

response = llm.generate(final_prompt, temperature=0.1)
```

---

## INTENT CLASSIFICATION

### Lightweight First Pass (Keywords)
```python
SALES_KEYWORDS = ["quote", "pricing", "price", "cost", "onboard", "get started", "contact sales", "buy", "purchase"]
INTERNAL_KEYWORDS = ["policy", "procedure", "internal", "staff", "employee", "guideline", "sop"]

if any(kw in query.lower() for kw in SALES_KEYWORDS):
    return "sales"
elif any(kw in query.lower() for kw in INTERNAL_KEYWORDS):
    return "internal"
else:
    return "support"
```

### Fallback (if ambiguous)
Use cheap LLM call with classification prompt.

---

## LEAD CAPTURE WORKFLOW

1. **Detection:** LLM response or user explicitly provides contact info
2. **Validation:** 
   - Email: regex check
   - Phone: basic format check (international OK)
3. **Storage:**
   - Append to Google Sheets
   - Send email notification to sales team
4. **Response:** Confirm to user

**Google Sheets columns:**
- Timestamp
- Email
- Phone
- Query/Interest
- Intent (support/sales/internal)
- Session ID (optional)

---

## ERROR HANDLING STRATEGY

### User-Facing Errors
```python
{
  "error": "I'm having trouble processing your request. Please try again or contact our team directly.",
  "error_code": "PROCESSING_ERROR"
}
```

### Internal Logging
```python
logger.error(
    "LLM API failure",
    extra={
        "query": query,
        "error": str(e),
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

### Graceful Degradation
- If RAG fails → return refusal message + escalation
- If LLM fails → return cached response or escalation
- If lead capture fails → log error, still return response to user

---

## TESTING STRATEGY

### Manual Testing (MVP)
- Test queries document: 50+ sample queries
- Cover all three modes
- Include edge cases
- Test refusal scenarios

### Key Test Cases
1. Simple FAQ (should answer)
2. Out-of-scope question (should refuse)
3. Lead qualification trigger (should capture)
4. Ambiguous query (should default to support)
5. Very long query (should handle gracefully)
6. Empty query (should reject)
7. Injection attempt (should sanitize)

---

## DEPLOYMENT CHECKLIST

**Before Deploy:**
- [ ] Environment variables configured
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Health endpoint working
- [ ] Logs structured and working
- [ ] Error handling tested
- [ ] Documents ingested into FAISS
- [ ] All prompts loaded correctly

**Post Deploy:**
- [ ] Monitor first 100 queries
- [ ] Check error rates
- [ ] Verify lead capture working
- [ ] Review response quality
- [ ] Check cost per query

---

## FUTURE ENHANCEMENTS (V2+)

**Not in MVP, but documented for later:**
- CRM integration (replace Google Sheets)
- Analytics dashboard
- Multi-language support
- Authentication for internal mode
- Chat history (with opt-in)
- More advanced RAG (re-ranking, hybrid search)
- A/B testing framework
- Feedback collection

---

## KEY REFERENCE DOCUMENTS

All located in `.claude/` folder:
1. `master_prompt.md` — Bot behavior rules (CRITICAL)
2. `decisions.md` — Why each choice was made
3. `architecture_overview.md` — System design
4. `document_ingestion_guide.md` — How to prepare docs
5. `progress.md` — Project milestones

**System prompts:**
- `system_support.txt`
- `system_sales.txt`
- `system_internal.txt`
- `refusal_template.txt`

---

## COMMON COPILOT QUERIES YOU MIGHT HAVE

**"Write the /chat endpoint"**
→ Refer to this context + architecture_overview.md

**"Implement RAG retrieval"**
→ Use FAISS, 500-1000 char chunks, top-k=3-5, cosine similarity

**"Create lead capture function"**
→ Google Sheets API + email, validate email/phone, log everything

**"Build intent classifier"**
→ Keyword-based first, LLM fallback, default to "support"

**"Write guardrails validation"**
→ Check for hallucination indicators, policy violations, off-topic responses

---

## CRITICAL REMINDERS

1. **Trust > Coverage** — Refuse when uncertain
2. **Context-only** — Never use general knowledge
3. **Neutral tone** — No marketing language
4. **Security first** — Validate, sanitize, log
5. **Keep it simple** — MVP scope, no feature creep

---

**This context should be referenced for ALL code generation in Project Dwight.**