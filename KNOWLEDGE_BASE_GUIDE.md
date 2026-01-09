# 📚 Knowledge Base Update Guide

## Overview

Project Dwight uses **RAG (Retrieval-Augmented Generation)** - this means the chatbot answers questions based on documents you provide. No training needed!

**To improve responses: Add/edit documents → Re-ingest → Done!**

---

## 📁 Knowledge Base Structure

```
data/
├── 1_customer_support/     # Customer-facing support docs
│   ├── faq.md
│   ├── contact_info.md
│   └── ...
├── 2_services_pricing/     # Service descriptions & pricing
│   ├── services_overview.md
│   ├── fcl_shipping.md
│   ├── lcl_shipping.md
│   └── ...
├── 3_sales_process/        # Sales-related info
│   ├── quote_process.md
│   └── ...
└── 4_internal_policies/    # Internal policies (for internal queries)
    ├── company_overview.md
    └── ...
```

---

## ✏️ How to Edit Documents

### Step 1: Find the Right Folder

| Topic | Folder |
|-------|--------|
| FAQs, tracking, support | `1_customer_support/` |
| Services, pricing, shipping | `2_services_pricing/` |
| Quotes, sales process | `3_sales_process/` |
| Company policies, internal | `4_internal_policies/` |

### Step 2: Edit or Create Markdown Files

**File Format:** Use `.md` (Markdown) files

**Example: `data/2_services_pricing/fcl_shipping.md`**
```markdown
# FCL (Full Container Load) Shipping

## What is FCL?
FCL means booking an entire container for your cargo. Ideal when you have enough goods to fill a 20ft or 40ft container.

## Benefits
- Exclusive use of container
- Faster transit (no consolidation)
- Lower risk of damage
- Better for high-volume shipments

## Container Sizes
| Size | Dimensions | Capacity |
|------|------------|----------|
| 20ft | 5.9m x 2.35m x 2.39m | ~33 CBM |
| 40ft | 12m x 2.35m x 2.39m | ~67 CBM |
| 40ft HC | 12m x 2.35m x 2.69m | ~76 CBM |

## Pricing Factors
- Origin/destination ports
- Container size
- Peak season surcharges
- Special cargo requirements

## How to Book
Contact our sales team at sales@tigerlogistics.in with:
- Origin and destination
- Cargo details (weight, volume)
- Preferred dates
```

### Step 3: Re-ingest Documents

After editing, run this command to update the chatbot:

```powershell
cd C:\Users\SauravPayal\project\Dwight\backend
.\venv\Scripts\python.exe scripts\ingest_documents.py
```

**Expected output:**
```
Processing documents from: C:\...\data
Found 14 markdown files
Created 166 chunks
Vector store saved successfully!
```

---

## 🎯 Best Practices for Documents

### DO ✅

1. **Use clear headings**
   ```markdown
   # Main Topic
   ## Subtopic
   ### Details
   ```

2. **Include specific details**
   - Prices, times, sizes
   - Step-by-step processes
   - Contact information

3. **Use tables for structured data**
   ```markdown
   | Route | Transit Time | Cost Range |
   |-------|--------------|------------|
   | Mumbai-Dubai | 3-5 days | $800-1200 |
   ```

4. **Add FAQs at the end of each doc**
   ```markdown
   ## Frequently Asked Questions

   **Q: How long does FCL shipping take?**
   A: Typically 2-4 weeks depending on route.
   ```

5. **Keep information current**
   - Update prices regularly
   - Add new services as they launch

### DON'T ❌

1. Don't use vague language
   - ❌ "Contact us for pricing"
   - ✅ "FCL rates start from $800 for 20ft containers"

2. Don't duplicate content across files
   - Keep one source of truth for each topic

3. Don't use images (not supported in RAG)
   - Use text descriptions instead

---

## 🔄 Quick Reference: Update Workflow

```
1. EDIT:   Open file in data/ folder
2. SAVE:   Save your changes
3. INGEST: Run ingest_documents.py
4. TEST:   Ask the chatbot your question
5. REFINE: If answer is wrong, improve the doc
```

### One-liner to re-ingest:
```powershell
cd C:\Users\SauravPayal\project\Dwight\backend; .\venv\Scripts\python.exe scripts\ingest_documents.py
```

---

## 📋 Audit Checklist

Use this to review your knowledge base:

### Customer Support (`1_customer_support/`)
- [ ] Contact information (email, phone, address)
- [ ] FAQ with common questions
- [ ] Tracking instructions
- [ ] Complaint handling process
- [ ] Working hours / response times

### Services & Pricing (`2_services_pricing/`)
- [ ] All services listed with descriptions
- [ ] FCL details (sizes, pricing factors)
- [ ] LCL details (minimum volume, consolidation)
- [ ] Air freight options
- [ ] Customs clearance services
- [ ] Special cargo (cold chain, hazmat, oversized)
- [ ] Transit times by route
- [ ] Price ranges or pricing factors

### Sales Process (`3_sales_process/`)
- [ ] How to get a quote
- [ ] Required information for quotes
- [ ] Booking process steps
- [ ] Payment terms
- [ ] Document requirements

### Internal Policies (`4_internal_policies/`)
- [ ] Company overview
- [ ] Key differentiators
- [ ] Certifications & accreditations
- [ ] Partner network

---

## 🧪 Testing Your Updates

After re-ingesting, test with these queries:

```
"What services do you offer?"
"How much does FCL shipping cost?"
"What's the transit time from Mumbai to London?"
"How do I track my shipment?"
"What documents do I need for customs?"
```

If the chatbot gives wrong or incomplete answers:
1. Check if the info is in your docs
2. Make sure it's clearly stated
3. Re-ingest and test again

---

## 📊 Current Knowledge Base Stats

To check your current stats:
```powershell
cd C:\Users\SauravPayal\project\Dwight\backend
.\venv\Scripts\python.exe -c "from core.rag_engine import rag_engine; print(f'Total chunks: {rag_engine.vector_store.index.ntotal if rag_engine.vector_store else 0}')"
```

---

## 🆘 Need Help?

- **Chatbot not answering correctly?** → Check if info is in docs, then re-ingest
- **Ingestion fails?** → Check for syntax errors in markdown files
- **Too slow?** → Keep documents focused, avoid very long files

---

## 📝 Template: New Service Document

Copy this template when adding a new service:

```markdown
# [Service Name]

## Overview
Brief description of the service (2-3 sentences).

## Key Features
- Feature 1
- Feature 2
- Feature 3

## How It Works
1. Step one
2. Step two
3. Step three

## Pricing
| Option | Price Range | Notes |
|--------|-------------|-------|
| Basic | $X - $Y | Description |
| Premium | $X - $Y | Description |

## Requirements
- Document 1
- Document 2

## Transit Time
Typical duration and factors affecting it.

## Contact
For [Service Name] inquiries: specific-email@tigerlogistics.in

## FAQ

**Q: Common question 1?**
A: Answer to question 1.

**Q: Common question 2?**
A: Answer to question 2.
```
