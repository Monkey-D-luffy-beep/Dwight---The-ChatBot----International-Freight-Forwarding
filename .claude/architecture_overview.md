# PROJECT DWIGHT - TECHNICAL ARCHITECTURE
## Tiger Logistics AI Assistant

**Last Updated:** 2025-12-31  
**Status:** Design Phase

---

## SYSTEM OVERVIEW

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │
       │ HTTPS
       ▼
┌─────────────────────┐
│  Chat Widget (JS)   │
│  Hosted on Netlify  │
└──────┬──────────────┘
       │
       │ API Call
       ▼
┌─────────────────────────────┐
│     FastAPI Backend         │
│  (Railway/Render)           │
│                             │
│  ┌─────────────────────┐   │
│  │  /chat endpoint     │   │
│  └──────┬──────────────┘   │
│         │                   │
│         ▼                   │
│  ┌─────────────────────┐   │
│  │ Intent Classifier   │   │
│  └──────┬──────────────┘   │
│         │                   │
│    ┌────┴────┬────────┐    │
│    ▼         ▼        ▼    │
│  Support   Sales  Internal │
│  Prompt    Prompt  Prompt  │
│    │         │        │    │
│    └────┬────┴────┬───┘    │
│         ▼         │        │
│  ┌─────────────┐ │        │
│  │  RAG Engine │ │        │
│  │   (FAISS)   │ │        │
│  └──────┬──────┘ │        │
│         │        │        │
│         ▼        ▼        │
│  ┌──────────────────┐    │
│  │   LLM (OpenAI)   │    │
│  └──────┬───────────┘    │
│         │                 │
│         ▼                 │
│  ┌──────────────────┐    │
│  │   Guardrails     │    │
│  └──────┬───────────┘    │
└─────────┼─────────────────┘
          │
          ▼
    ┌─────────────┐
    │  Response   │
    │  to User    │
    └─────────────┘
          │
    (If lead detected)
          │
          ▼
    ┌─────────────────┐
    │  Google Sheets  │
    │  + Email        │
    └─────────────────┘
```

---

## TECH STACK (LOCKED)

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **RAG Framework:** LangChain (or custom lightweight implementation)
- **Vector Store:** FAISS (local, in-memory)
- **LLM:** OpenAI GPT-4o-mini (initial)
- **Environment:** .env file for secrets

### Frontend
- **UI:** Plain HTML + CSS + JavaScript
- **Hosting:** Netlify or Vercel
- **Type:** Floating chat widget (embeddable via script tag)

### Infrastructure
- **Backend Hosting:** Railway or Render
- **Domain:** chat.tigerlogistics.com (or subdomain)
- **SSL:** Automatic via hosting platform
- **Database:** None (stateless for MVP)

### Integrations
- **Email:** SMTP (Gmail/SendGrid)
- **Sheets:** Google Sheets API (for lead logging)
- **Future:** CRM webhook (Salesforce, HubSpot)

---

## PROJECT STRUCTURE

```
project_dwight/
│
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration and environment variables
│   ├── requirements.txt           # Python dependencies
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py                # /chat endpoint
│   │   └── health.py              # /health endpoint
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── intent_classifier.py  # Detect support/sales/internal mode
│   │   ├── rag_engine.py         # Document retrieval logic
│   │   ├── embeddings.py         # Generate and search embeddings
│   │   ├── llm_client.py         # OpenAI API wrapper
│   │   └── guardrails.py         # Response validation and refusal logic
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── lead_capture.py       # Google Sheets + email logic
│   │   └── logger.py             # Structured logging
│   │
│   ├── prompts/
│   │   ├── system_support.txt    # Customer support system prompt
│   │   ├── system_sales.txt      # Sales system prompt
│   │   ├── system_internal.txt   # Internal knowledge system prompt
│   │   └── refusal_template.txt  # Refusal/uncertainty handling
│   │
│   ├── data/
│   │   ├── raw_docs/
│   │   │   ├── 1_customer_support/
│   │   │   ├── 2_services_pricing/
│   │   │   ├── 3_sales_process/
│   │   │   └── 4_internal_policies/
│   │   │
│   │   └── processed/
│   │       └── faiss_index/       # FAISS vector store files
│   │
│   ├── tests/
│   │   ├── test_intent.py
│   │   ├── test_rag.py
│   │   └── test_api.py
│   │
│   └── scripts/
│       ├── ingest_documents.py    # Convert docs → embeddings
│       └── test_queries.py        # Manual testing script
│
├── frontend/
│   ├── index.html                 # Standalone chat page (for testing)
│   ├── widget.html                # Embeddable widget version
│   ├── widget.js                  # Main chat widget logic
│   ├── widget.css                 # Styling
│   └── assets/
│       └── logo.svg               # Tiger Logistics logo
│
├── docs/
│   ├── master_prompt.md           # Master prompt document
│   ├── progress.md                # Project progress tracker
│   ├── decisions.md               # Decision log
│   ├── document_ingestion_guide.md
│   └── architecture_overview.md  # This file
│
├── .env.example                   # Example environment variables
├── .gitignore
├── README.md
└── LICENSE
```

---

## KEY COMPONENTS EXPLAINED

### 1. Intent Classifier (`intent_classifier.py`)

**Purpose:** Automatically determine if query is customer support, sales, or internal.

**Approach:** 
- Lightweight keyword/pattern matching first (fast, cheap)
- If ambiguous, use cheap LLM classification call
- Default to "customer support" if uncertain

**Example logic:**
```python
def classify_intent(query: str) -> str:
    query_lower = query.lower()
    
    # Sales keywords
    if any(word in query_lower for word in ["quote", "pricing", "onboard", "get started", "contact sales"]):
        return "sales"
    
    # Internal keywords
    if any(word in query_lower for word in ["policy", "procedure", "internal", "staff", "employee"]):
        return "internal"
    
    # Default
    return "support"
```

---

### 2. RAG Engine (`rag_engine.py`)

**Purpose:** Retrieve relevant document chunks for a given query.

**Flow:**
1. User query → embedding
2. Similarity search in FAISS
3. Return top 3-5 relevant chunks
4. Pass chunks as context to LLM

**Key parameters:**
- Chunk size: 500-1000 characters
- Overlap: 100 characters
- Top-k results: 3-5

---

### 3. LLM Client (`llm_client.py`)

**Purpose:** Wrapper around OpenAI API.

**Features:**
- Temperature control (0.0-0.2 for factual responses)
- Token limit enforcement
- Retry logic
- Cost tracking

**Example function:**
```python
def generate_response(
    system_prompt: str,
    context: str,
    query: str,
    temperature: float = 0.1
) -> str:
    # Call OpenAI API
    # Return response text
```

---

### 4. Guardrails (`guardrails.py`)

**Purpose:** Validate LLM output before returning to user.

**Checks:**
1. Response is not empty
2. Response does not contain hallucination indicators
3. Response does not make unauthorized promises
4. Response triggers refusal if needed

**Rejection triggers:**
- LLM says "I don't have information in the provided context"
- Response contradicts known policies
- Response is off-topic

---

### 5. Lead Capture (`lead_capture.py`)

**Purpose:** Save qualified leads to Google Sheets and send email notification.

**Flow:**
1. Detect lead intent (from LLM response or explicit user action)
2. Validate email/phone format
3. Write to Google Sheets
4. Send email to sales team
5. Return confirmation to user

**Data stored:**
- Timestamp
- Email
- Phone
- Query/interest area
- Conversation context (optional)

---

### 6. Chat Widget (`widget.js`)

**Purpose:** Embeddable chat interface.

**Features:**
- Floating bubble (bottom-right corner)
- Expand/collapse
- Message history (session-only)
- Typing indicator
- Error handling
- Mobile responsive

**Embedding code for company website:**
```html
<script src="https://chat.tigerlogistics.com/widget.js"></script>
```

---

## API ENDPOINTS

### `POST /chat`
**Purpose:** Main chat interface.

**Request:**
```json
{
  "query": "How long does sea freight take?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Sea freight transit times vary by route...",
  "intent": "support",
  "lead_captured": false,
  "metadata": {
    "tokens_used": 245,
    "confidence": 0.92
  }
}
```

---

### `GET /health`
**Purpose:** Health check for monitoring.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-12-31T10:00:00Z"
}
```

---

## SECURITY CONSIDERATIONS

### API Security
- Rate limiting (100 requests/hour per IP for MVP)
- CORS properly configured
- No sensitive data in logs
- Environment variables for all secrets

### Input Validation
- Sanitize user inputs
- Reject excessively long queries (>1000 chars)
- Validate email/phone formats

### Data Privacy
- No chat history stored (stateless)
- Leads stored securely (Google Sheets with restricted access)
- No PII in logs

---

## DEPLOYMENT STRATEGY

### Phase 1: Development
- Run locally on `localhost:8000`
- Test with sample documents
- Manual testing with test queries

### Phase 2: Staging
- Deploy to Railway/Render (free tier)
- Use subdomain: `staging.chat.tigerlogistics.com`
- Internal team testing

### Phase 3: Production
- Deploy to production environment
- Use domain: `chat.tigerlogistics.com`
- Monitor for 1 week before website integration

### Phase 4: Integration
- Embed on Tiger Logistics main website
- Monitor usage and errors
- Iterate based on feedback

---

## COST ESTIMATES (MONTHLY)

**Infrastructure:**
- Railway/Render backend: $5-10
- Netlify frontend: $0 (free tier)
- Domain: $1

**API Costs (at 100 queries/day):**
- OpenAI GPT-4o-mini: ~$15-20
- Embeddings: ~$2

**Total:** ~$25-35/month for MVP

**Scaling:** At 1000 queries/day, estimate ~$100-150/month.

---

## MONITORING & LOGGING

**What to track:**
- Request count per endpoint
- Response times
- Error rates
- Token usage per query
- Intent distribution (support vs sales vs internal)
- Lead conversion rate
- Top unanswered queries (for knowledge base improvement)

**Tools:**
- Python logging module (structured JSON logs)
- Railway/Render built-in logs
- Optional: Sentry for error tracking

---

## DEVELOPMENT WORKFLOW

1. **Document preparation** (Week 1)
2. **Backend skeleton** (Week 2)
3. **RAG implementation** (Week 2)
4. **Frontend widget** (Week 3)
5. **Integration testing** (Week 4)
6. **Deployment** (Week 5)
7. **Company integration** (Week 6)

---

## NEXT STEPS

1. Set up Python environment
2. Install dependencies
3. Create project structure
4. Implement document ingestion script
5. Build /chat endpoint skeleton
6. Test with sample query

---

**Ready to start coding once documents are prepared.**