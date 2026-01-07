# PROJECT DWIGHT - DECISION LOG
## Tiger Logistics AI Assistant

**Purpose:** Document every major decision and the reasoning behind it.  
**Audience:** Future developers, management, auditors.

---

## STRATEGIC DECISIONS

### ✅ One Chatbot, Three Modes
**Decision:** Build a single unified assistant with automatic intent detection, not three separate bots.

**Reasoning:**
- Cleaner user experience (no dropdown menus)
- Easier to embed on website
- Simpler maintenance
- Demonstrates intelligence to management
- Future-proof for expansion

**Trade-off:** Slightly more complex backend logic, but worth it.

---

### ✅ RAG-Only, No Fine-Tuning
**Decision:** Use Retrieval-Augmented Generation (RAG) exclusively. No model fine-tuning.

**Reasoning:**
- Faster to build and iterate
- Much cheaper (no training costs)
- Easier to update knowledge (just swap documents)
- Lower technical complexity
- Perfectly adequate for this use case

**When to reconsider:** If query volume exceeds 10,000/day or latency becomes critical.

---

### ✅ Separate Domain First, Integration Later
**Decision:** Launch on `chat.tigerlogistics.com` (or similar) before embedding on main site.

**Reasoning:**
- Zero dependency on vendor timeline
- Can demo and prove value independently
- Easier testing and iteration
- Reduces vendor objections (just 1 script tag later)
- Keeps control in-house

**Integration plan:** Phase 6, after MVP validation.

---

## TECHNICAL DECISIONS

### ✅ Python + FastAPI
**Decision:** Backend in Python with FastAPI framework.

**Reasoning:**
- Best ecosystem for AI/ML work
- Fast development speed
- Your existing Python knowledge
- Excellent async support
- Easy deployment

**Alternatives considered:**
- Node.js: Less mature AI ecosystem
- Django: Overkill for API-only service

---

### ✅ FAISS for Vector Storage
**Decision:** Use local FAISS for vector embeddings (not Pinecone, Weaviate, etc.).

**Reasoning:**
- Zero cost
- Fast for <10,000 documents
- No external dependencies
- Simple deployment
- Easy to migrate later if needed

**When to upgrade:** If document count exceeds 50,000 or need multi-user filtering.

---

### ✅ OpenAI GPT-4o-mini (Initial Model)
**Decision:** Start with OpenAI's GPT-4o-mini for cost efficiency.

**Reasoning:**
- Cost: ~$0.15 per 1M input tokens
- Quality: Sufficient for structured queries
- Reliability: Production-ready
- Speed: Fast responses

**Future optimization:**
- Route simple FAQs to even cheaper models
- Use GPT-4 only for complex sales queries
- Consider Claude for longer contexts

---

### ✅ No Chat History Persistence
**Decision:** Do not store conversation history between sessions.

**Reasoning:**
- Simpler architecture (stateless)
- No database needed for MVP
- No privacy concerns
- Lower infrastructure cost
- Faster development

**Trade-off:** Users must repeat context if they refresh. Acceptable for MVP.

---

### ✅ No Source Citations in UI
**Decision:** Don't show "Source: page 5" in responses.

**Reasoning:**
- Cleaner user experience
- Less cognitive load
- RAG still grounds responses internally
- Sources logged on backend for debugging

**When to reconsider:** If management specifically requests transparency or for compliance reasons.

---

## SAFETY & GUARDRAIL DECISIONS

### ✅ Strict Context-Only Answering
**Decision:** Bot must ONLY answer from provided documents. No general knowledge.

**Reasoning:**
- Prevents hallucination
- Builds trust with management
- Reduces legal/compliance risk
- Makes quality measurable (either in docs or not)

**Implementation:** Hard-coded in master prompt + enforced in code.

---

### ✅ Explicit "I Don't Know" Responses
**Decision:** Bot must confidently refuse when information is not in context.

**Reasoning:**
- Better to say "I don't know" than to be wrong
- Encourages human escalation (which is desired)
- Protects company reputation
- Identifies knowledge gaps for improvement

**Phrasing:** "I don't have confirmed information on that at the moment. I can connect you with our team if you'd like."

---

### ✅ Proactive Lead Capture Only on Intent
**Decision:** Bot asks for contact info only when user shows buying intent or requests escalation.

**Reasoning:**
- Less annoying than popup forms
- Higher quality leads
- Better user experience
- Respects user autonomy

**Triggers:**
- User asks about pricing, quotes, onboarding
- User asks "how do I proceed?"
- User explicitly asks for human contact

---

## BUSINESS DECISIONS

### ✅ Lead Routing: Single Email + Google Sheets
**Decision:** V1 sends leads to one email and logs to Google Sheets. No CRM yet.

**Reasoning:**
- Fastest to implement
- No CRM vendor dependency
- Easy to manually review
- Simple to add CRM later (same pipeline)

**V2 plan:** Add Salesforce/HubSpot integration once proven.

---

### ✅ Neutral Tone (Not Friendly, Not Formal)
**Decision:** Bot uses neutral, professional language.

**Reasoning:**
- Matches freight forwarding industry norms
- Avoids sounding too casual (unprofessional)
- Avoids sounding too stiff (robotic)
- Internationally acceptable
- Reduces cultural misinterpretation risk

**Examples:**
- ❌ "Hey! 😊 Let me help you with that!"
- ❌ "Pursuant to our operational guidelines..."
- ✅ "I can help you with that. Here's what you need to know:"

---

### ✅ Email + Phone for Leads (Not Just Email)
**Decision:** Capture both email and phone number.

**Reasoning:**
- Sales team prefers phone contact for freight quotes
- Higher conversion rate with phone follow-up
- International clients often prefer WhatsApp (phone-based)
- Still optional—user can skip if uncomfortable

---

## SCOPE DECISIONS (WHAT WE'RE NOT BUILDING)

### ❌ No Authentication System
**Decision:** No login/passwords for MVP.

**Reasoning:**
- Not needed for customer-facing support
- Adds complexity
- Delays launch
- Can add later for internal-only features

---

### ❌ No Multi-Language Support
**Decision:** English only for V1.

**Reasoning:**
- Tiger Logistics operates internationally, but English is business standard
- Translation adds cost and complexity
- Can be added in V2 with proper localization

---

### ❌ No Real-Time Order Tracking
**Decision:** Bot does not integrate with order/shipment databases.

**Reasoning:**
- Requires database access (security risk)
- Requires authentication (scope creep)
- Dynamic data = different architecture
- V1 is knowledge-based only

**Alternative:** Bot can explain how customers track orders and link to portal.

---

### ❌ No Analytics Dashboard
**Decision:** No custom analytics UI for MVP.

**Reasoning:**
- Can use Google Sheets + backend logs initially
- Delays launch
- Management doesn't need it yet

**V2:** Build simple dashboard once usage patterns are understood.

---

## DEPLOYMENT DECISIONS

### ✅ Railway/Render for Hosting
**Decision:** Use Railway or Render for backend deployment.

**Reasoning:**
- Cheap (~$5-10/month)
- Easy Python support
- Auto-deployment from Git
- Good uptime
- No DevOps complexity

**Alternatives considered:**
- AWS: Overkill and expensive for MVP
- Heroku: More expensive
- VPS: Requires manual maintenance

---

### ✅ Netlify/Vercel for Frontend Widget
**Decision:** Host chat widget on Netlify or Vercel.

**Reasoning:**
- Free for low traffic
- CDN included
- Fast global delivery
- Easy SSL
- One-command deployment

---

## TESTING DECISIONS

### ✅ Manual Testing for MVP
**Decision:** No automated test suite for V1.

**Reasoning:**
- Faster to ship
- Can manually test 20 documents easily
- Automated tests add development time
- Better to validate concept first

**V2:** Add unit tests and integration tests once core is stable.

---

## COST DECISIONS

### ✅ Target: <$50/month Operating Cost
**Decision:** MVP must run for under $50/month all-in.

**Reasoning:**
- Makes internal approval easier
- Proves cost efficiency
- Sustainable for testing period
- Easy to justify to finance

**Cost breakdown estimate:**
- Hosting: $5-10
- LLM API: $10-20 (at 100 queries/day)
- Domain: $1
- Buffer: $20

---

## KEY PRINCIPLES (NEVER COMPROMISE)

1. **Trust over coverage** — Better to say "I don't know" than to be wrong
2. **Simplicity over features** — Ship fast, iterate based on real usage
3. **Context-only answers** — No hallucinations, ever
4. **Clear escalation paths** — Always offer human handoff
5. **No vendor lock-in** — Keep control of the entire stack

---

## DECISION AUTHORITY

**Technical decisions:** Developer (you) with stakeholder review  
**Business decisions:** Management approval required  
**Scope decisions:** Jointly agreed

---

## CHANGELOG

**2025-12-31:** Initial decision log created  
**Future:** Update as project evolves