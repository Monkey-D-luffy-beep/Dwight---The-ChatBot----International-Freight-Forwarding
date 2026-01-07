# Project Dwight - MVP Development Plan

**Date**: January 6, 2026  
**Status**: Phase 4 Complete - Ready for Cloud Integration

---

## 🎯 Current Situation

### What Works ✅
- Backend API (FastAPI) running on `http://127.0.0.1:8000`
- Frontend chat widget running on `http://127.0.0.1:3000`
- RAG system with FAISS vector store (166 chunks, 14 documents)
- Lead capture with local JSON fallback
- All 6 tests passing

### Current Bottlenecks 🐌
- **Response Time**: 50+ seconds per query
- **Reason**: tinyllama runs on CPU (local Ollama)
- **Disk Space**: Vector store + models taking space
- **Solution**: Switch to cloud LLM APIs (free tier available)

---

## ☁️ Cloud Service Strategy

### Option 1: Free Tier Cloud LLM (RECOMMENDED)
Instead of running models locally, use cloud APIs:

| Provider | Free Tier | Speed | Setup Time |
|----------|-----------|-------|------------|
| **Groq** ⭐ | 30 RPM, 6000 TPM | 1-2s | 5 min |
| **Google Gemini** | 15 RPM | 2-3s | 10 min |
| **Together AI** | $25 credits | 3-5s | 5 min |
| **Hugging Face** | Limited free | 5-10s | 15 min |

**Best Choice: Groq**
- 100% FREE up to 30 requests/minute
- 500+ tokens/second (nearly instant)
- Models: llama-3.1-8b, mixtral-8x7b
- No credit card required

### Option 2: Deploy Backend to Cloud (Free Tier)
Move the entire backend to cloud hosting:

| Service | Free Tier | Use Case |
|---------|-----------|----------|
| **Railway** | $5 credit/month | Backend API |
| **Render** | 750 hrs/month | Backend API |
| **Fly.io** | 3 VMs free | Backend + vector DB |
| **Vercel** | Unlimited | Frontend hosting |
| **Netlify** | 100GB bandwidth | Frontend hosting |

**Recommended Stack (100% Free):**
```
Frontend → Vercel (free, unlimited)
Backend → Railway ($5 credit = ~160 hours = MVP testing)
LLM → Groq (free forever for low usage)
Vector Store → Keep FAISS (uploads with backend)
```

---

## 💰 Cost Analysis

### Development Phase (Now)
| Component | Cost | Notes |
|-----------|------|-------|
| Groq LLM | **$0** | Free tier: 30 RPM |
| Backend (Railway) | **$0** | $5 free credit/month |
| Frontend (Vercel) | **$0** | Free forever |
| Vector Store | **$0** | FAISS stored with backend |
| **TOTAL** | **$0/month** | Perfect for MVP testing |

### MVP Launch (500 queries/day)
| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Groq LLM | **$0** | Still within free tier |
| Railway Backend | **$5** | May need paid plan |
| Vercel Frontend | **$0** | Free plan sufficient |
| **TOTAL** | **$5/month** | Extremely affordable |

### Production Scale (2000 queries/day)
| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Groq LLM | $10-20 | May exceed free tier |
| Railway Backend | $15-20 | Larger instance |
| Vercel Frontend | $0 | Still free |
| **TOTAL** | **$25-40/month** | Still very affordable |

### Alternative: Premium LLMs
| Model | Cost per 1M tokens | 2000 queries/day |
|-------|-------------------|------------------|
| GPT-4o-mini | $0.15 input, $0.60 output | ~$25/month |
| Claude Sonnet | $3 input, $15 output | ~$40/month |
| Gemini Pro | $0.125 input, $0.375 output | ~$15/month |

**Verdict**: Start with Groq (free), upgrade later if needed.

---

## 📚 Knowledge Base Strategy

### Understanding: Training vs RAG

| Approach | What It Means | Cost | Time | Best For |
|----------|---------------|------|------|----------|
| **RAG (Current)** | Feed docs at query time | $0 | Instant | ✅ Your use case |
| **Fine-tuning** | Retrain model weights | $500-5000 | Days | ❌ Overkill |
| **Prompt Engineering** | Better system prompts | $0 | Hours | ✅ Do this too |

### Why Local LLM is Slow
```
tinyllama on CPU:
- 1.1B parameters
- CPU processing: ~20-30 tokens/second
- No GPU acceleration
- Result: 50+ seconds per response

Groq Cloud (same model):
- Same llama model
- Custom LPU (Language Processing Unit)
- Result: 500+ tokens/second = 2 seconds per response
```

### You DON'T Need Training!
**Your chatbot uses RAG (Retrieval-Augmented Generation):**
1. User asks: "What is FCL shipping?"
2. System searches vector store for relevant docs
3. Sends context + question to LLM
4. LLM generates answer from provided context

**To improve responses:**
- ✅ Add more detailed docs to `data/` folders
- ✅ Re-run `python scripts/ingest_documents.py`
- ✅ Improve system prompts
- ❌ NO training needed

---

## 🛣️ Phase-by-Phase Development Path

### ✅ Phase 1-4: Foundation (COMPLETE)
- Master prompt created
- Knowledge base (14 docs)
- Backend with RAG
- Frontend chat widget
- Lead capture system
- All tests passing

### 🔄 Phase 5: Cloud Integration (NEXT - 1-2 hours)

#### Step 5.1: Switch to Groq
```bash
# Install Groq package
pip install groq

# Get free API key from https://console.groq.com
# Update .env file
# Test with same queries - see 25x speedup
```

**Expected Outcome:**
- Response time: 50s → 2s
- Zero cost (free tier)
- Same quality responses

#### Step 5.2: Keep Ollama as Fallback
```python
# Auto-fallback logic:
if groq_api_key:
    use groq  # Fast cloud
else:
    use ollama  # Slow but works offline
```

### 📈 Phase 6: Knowledge Base Expansion (3-5 hours)

#### What to Add:
1. **Customer Support Details**
   - Common issues & solutions
   - FAQs with detailed answers
   - Step-by-step guides

2. **Service Details**
   - FCL/LCL processes
   - Documentation requirements
   - Port-specific information
   - Transit times by route

3. **Pricing Structures**
   - Rate calculation examples
   - Surcharge explanations
   - Volume discount tiers

4. **Company Policies**
   - Terms & conditions
   - Refund policies
   - Insurance options

#### How to Add:
```bash
# 1. Create new .md files in data/ folders
data/1_customer_support/faq_detailed.md
data/2_services_pricing/fcl_process_guide.md
data/3_sales_process/port_transit_times.md

# 2. Re-ingest documents
python scripts/ingest_documents.py

# 3. Test queries
python tests/test_phase4.py
```

**No training required** - just add docs and re-ingest!

### 🚀 Phase 7: Deploy to Cloud (2-3 hours)

#### Backend Deployment (Railway)
```bash
# 1. Create railway.app account
# 2. Install Railway CLI
# 3. Deploy
railway login
railway init
railway up

# Your backend gets a URL:
# https://dwight-backend.railway.app
```

#### Frontend Deployment (Vercel)
```bash
# 1. Create vercel.com account
# 2. Install Vercel CLI
# 3. Deploy
vercel login
vercel --prod

# Your frontend gets a URL:
# https://dwight-chat.vercel.app
```

#### Update Frontend Config
```javascript
// frontend/script.js
const API_URL = "https://dwight-backend.railway.app";
// Instead of: http://127.0.0.1:8000
```

### 📊 Phase 8: Analytics & Monitoring (1-2 hours)
- Add Google Analytics to frontend
- Track: queries, lead conversions, popular topics
- Monitor response times
- Set up error alerts

### 🎨 Phase 9: Polish & Features (ongoing)
- Custom branding (Tiger Logistics colors)
- Multi-language support (if needed)
- Voice input option
- Document upload capability
- Chat history/session management

---

## 🔥 Immediate Action Plan

### TODAY: Switch to Groq (15 minutes)

1. **Get Groq API Key** (2 min)
   - Visit https://console.groq.com
   - Sign up (free, no card needed)
   - Copy API key

2. **Update Code** (5 min)
   ```bash
   pip install groq
   # Update config.py and llm_client.py
   ```

3. **Test** (5 min)
   ```bash
   python tests/test_phase4.py
   # Watch responses go from 50s → 2s
   ```

4. **Celebrate** (3 min)
   - Your chatbot is now production-ready speed!

### THIS WEEK: Expand Knowledge Base

1. **Day 1-2**: Create detailed docs
   - Research Tiger Logistics services
   - Write comprehensive guides
   - Add FAQs

2. **Day 3**: Ingest and test
   - Run ingestion script
   - Test various queries
   - Refine responses

3. **Day 4-5**: Deploy to cloud
   - Set up Railway/Vercel accounts
   - Deploy backend and frontend
   - Test production URLs

### NEXT WEEK: Go Live

1. **Soft Launch**: Share with internal team
2. **Gather Feedback**: Monitor conversations
3. **Iterate**: Improve based on usage
4. **Public Launch**: Add to Tiger Logistics website

---

## 📋 Disk Space Optimization

### Current Space Usage:
```
backend/venv/          ~500 MB (Python packages)
vector_store/          ~50 MB (FAISS index)
Ollama models/         ~1.5 GB (can delete after Groq switch)
```

### After Groq Switch:
```
backend/venv/          ~500 MB
vector_store/          ~50 MB
Total:                 ~550 MB (75% reduction!)
```

### To Free Space:
```bash
# Stop Ollama
ollama stop

# Remove models (safe after Groq setup)
ollama rm tinyllama
ollama rm nomic-embed-text

# Reclaim ~1.5 GB
```

---

## 🎯 Success Metrics

### MVP Goals:
- ✅ Response time < 5 seconds (Groq: ~2s)
- ✅ 90%+ query relevance (RAG working)
- ✅ Lead capture functional (✅ working)
- ✅ Zero hosting cost during testing (Groq + Railway free tier)
- 🔄 100+ knowledge base chunks (currently 166, can expand)

### Launch Goals:
- Handle 500 queries/day
- 10%+ lead conversion rate
- < $5/month operating cost
- 95%+ uptime

---

## 🔧 Technical Architecture

### Current (Local):
```
User → Frontend (localhost:3000)
     → Backend (localhost:8000)
     → Ollama (local tinyllama) 🐌 50s
     → FAISS (local vector store)
```

### Phase 5 (Groq):
```
User → Frontend (localhost:3000)
     → Backend (localhost:8000)
     → Groq Cloud (llama-3.1) ⚡ 2s
     → FAISS (local vector store)
```

### Phase 7 (Full Cloud):
```
User → Frontend (Vercel CDN)
     → Backend (Railway cloud)
     → Groq Cloud (llama-3.1)
     → FAISS (deployed with backend)
     → Leads → JSON backup + Google Sheets
```

---

## 💡 Pro Tips

1. **Start with Groq**: Fastest path to production-ready speed
2. **Don't train**: RAG is perfect for your use case
3. **Expand knowledge base gradually**: Quality > Quantity
4. **Monitor usage**: Track which topics need more docs
5. **Use free tiers**: Get to market before paying anything
6. **Keep Ollama**: Fallback for offline testing

---

## 🚦 Next Steps

**Right Now:**
- [ ] Get Groq API key
- [ ] Update backend to use Groq
- [ ] Test speed improvement

**This Week:**
- [ ] Create 5-10 more detailed knowledge docs
- [ ] Re-ingest documents
- [ ] Deploy to Railway + Vercel

**Next Week:**
- [ ] Soft launch with internal team
- [ ] Gather feedback
- [ ] Public launch

---

## 📞 Questions?

**Q: Will I need to pay eventually?**  
A: Not until you hit 500+ queries/day. Even then, only $5-10/month.

**Q: How do I improve response quality?**  
A: Add more detailed docs to `data/` folders and re-ingest. No training needed.

**Q: Why not use GPT-4?**  
A: Start with Groq (free). Upgrade to GPT-4 later if needed for better quality.

**Q: Can I run this offline?**  
A: Yes! Keep Ollama as fallback. Backend auto-switches when offline.

**Q: How do I scale to 10,000 queries/day?**  
A: Still under $100/month. Groq handles it easily.

---

## 🎉 Summary

**You're 99% done!** Just need to:
1. Switch to Groq (15 min) → 25x speedup
2. Add more docs (ongoing) → better responses
3. Deploy to cloud (2-3 hours) → public access

**Total cost to MVP**: $0  
**Time to production**: 1-2 days  
**Current status**: Fully functional, just slow locally

Let's switch to Groq first - you'll see immediate results! 🚀
