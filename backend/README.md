# Project Dwight - Backend

Tiger Logistics AI Assistant Backend

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Ingest Documents

```bash
# Build the vector store from documents
python scripts/ingest_documents.py
```

### 4. Run the Server

```bash
# Development mode
uvicorn main:app --reload --port 8000

# Or directly
python main.py
```

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services does Tiger Logistics offer?"}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI entry point
├── config.py            # Configuration management
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
│
├── routers/
│   ├── chat.py          # Chat API endpoints
│   └── health.py        # Health check endpoints
│
├── core/
│   ├── intent_classifier.py  # Intent detection
│   ├── rag_engine.py         # Document retrieval
│   ├── embeddings.py         # Vector generation
│   ├── llm_client.py         # LLM interaction
│   └── guardrails.py         # Response validation
│
├── services/
│   ├── lead_capture.py   # Lead storage
│   └── logger.py         # Logging service
│
└── scripts/
    ├── ingest_documents.py   # Build vector store
    └── test_queries.py       # Test the pipeline
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/health/ready` | Readiness check |
| POST | `/api/chat` | Main chat endpoint |
| POST | `/api/lead` | Lead capture |

## Configuration

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LLM_MODEL` | LLM model to use | gpt-4o-mini |
| `LLM_TEMPERATURE` | Response randomness | 0.1 |
| `TOP_K_RESULTS` | RAG results to retrieve | 3 |

## Development

```bash
# Run tests
python scripts/test_queries.py

# Format code
black .

# Lint
flake8 .
```
