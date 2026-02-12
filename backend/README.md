# Backend

FastAPI service that powers the GTMT chatbot — intent classification → RAG retrieval → LLM response → guardrails.

## Setup

```bash
python -m venv venv && source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
python scripts/ingest_documents.py   # build the FAISS index
uvicorn main:app --reload --port 8000
```

## Endpoints

| Method | Path | What it does |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/health/ready` | Readiness (RAG loaded?) |
| POST | `/api/chat` | Main chat |
| POST | `/api/lead` | Lead capture |

# Format code
black .

# Lint
flake8 .
```
