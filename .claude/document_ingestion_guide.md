# DOCUMENT INGESTION GUIDE
## Project Dwight - Tiger Logistics

**Purpose:** How to prepare, structure, and organize knowledge documents for optimal RAG performance.

---

## DOCUMENT ORGANIZATION STRATEGY

### Required Structure
```
data/
├── raw_docs/
│   ├── 1_customer_support/
│   ├── 2_services_pricing/
│   ├── 3_sales_process/
│   └── 4_internal_policies/
└── processed/
    └── embeddings/
```



---

## THE 4 KNOWLEDGE BUCKETS

### **Bucket 1: Customer Support FAQs**
**Purpose:** Common questions customers ask

**Examples:**
- How do I track my shipment?
- What documents do I need for customs clearance?
- What are your operating hours?
- How do I file a claim?
- What's the difference between sea and air freight?

**Format:** FAQ pairs (Question + Answer)

**Recommended files:**
- `customer_faq.md`
- `tracking_guide.md`
- `documentation_requirements.md`

---

### **Bucket 2: Services & Pricing**
**Purpose:** What Tiger Logistics offers and how pricing works

**Examples:**
- Sea freight services
- Air cargo services
- Customs brokerage
- Warehousing and distribution
- Insurance options
- Service geographic coverage

**Format:** Service descriptions with structured details

**Recommended files:**
- `sea_freight_services.md`
- `air_cargo_services.md`
- `customs_clearance.md`
- `pricing_structure.md` (general framework, not exact quotes)
- `service_areas.md`

**⚠️ CRITICAL:** No exact prices—only pricing models (e.g., "calculated by weight, distance, and urgency")

---

### **Bucket 3: Sales Process & Onboarding**
**Purpose:** How new customers get started

**Examples:**
- How to request a quote
- Onboarding steps
- Required information from customers
- Contract terms overview
- Payment terms
- Contact information for sales team

**Format:** Process flows and requirements

**Recommended files:**
- `how_to_get_quote.md`
- `onboarding_process.md`
- `required_customer_info.md`
- `payment_terms.md`

---

### **Bucket 4: Internal Policies**
**Purpose:** Information for Tiger Logistics staff

**Examples:**
- Operational procedures
- Escalation protocols
- System access guidelines
- Internal communication standards
- Quality standards

**Format:** Policy documents and SOPs

**Recommended files:**
- `internal_procedures.md`
- `escalation_policy.md`
- `quality_standards.md`

**⚠️ Note:** These should be less sensitive internal docs—no financial data or confidential strategy.

---

## DOCUMENT FORMATTING RULES

### ✅ DO:
- Use **Markdown** (.md) or plain text (.txt)
- Keep language clear and concise
- Use headings and subheadings
- Include concrete examples
- Write in neutral, professional tone
- Use bullet points for lists
- Keep paragraphs short (2-4 sentences)

### ❌ DON'T:
- Use complex formatting (tables, images, etc. for MVP)
- Include outdated information
- Use ambiguous language ("might", "could", "sometimes")
- Mix multiple topics in one file
- Use marketing fluff
- Include contact info that might change (centralize in one file)

---

## DOCUMENT TEMPLATE EXAMPLES

### Example 1: FAQ Document
```markdown
# Sea Freight FAQ

## How long does sea freight take?

Sea freight transit times vary by route:
- Asia to US West Coast: 14-18 days
- Asia to US East Coast: 28-35 days  
- Europe to US: 12-16 days

Transit time starts when the vessel departs the origin port.

## What's the maximum weight for a sea freight container?

Standard 20ft container: Maximum 28,000 kg (approx. 28 tons)
Standard 40ft container: Maximum 28,000 kg (approx. 28 tons)

The container weight limit is based on road transport regulations, not the container's physical capacity.

## Can I ship hazardous materials by sea?

Yes, but hazardous materials require:
- Proper classification and declaration
- Special packaging and labeling
- Additional documentation (MSDS, dangerous goods declaration)
- Advanced booking confirmation

Contact our team for hazardous cargo quotes.
```

---

### Example 2: Service Description
```markdown
# Customs Clearance Services

## Overview
Tiger Logistics provides full customs brokerage services for import and export shipments.

## What We Handle
- Classification and valuation
- Documentation preparation and submission
- Duty and tax calculation
- Customs inspections coordination
- Release and delivery coordination

## Required Documents
From customer:
- Commercial invoice
- Packing list
- Bill of lading / Air waybill
- Certificate of origin (if applicable)
- Import license (if required by commodity)

## Processing Time
- Standard clearance: 1-3 business days
- Pre-clearance (if arranged): Same day as arrival
- Inspections may add 1-2 days

## Geographic Coverage
We provide customs clearance at:
- All major US ports
- All major European ports
- Selected Asian ports (contact for specific locations)
```

---

### Example 3: Sales Process
```markdown
# How to Request a Quote

## Step 1: Gather Shipment Details
Before requesting a quote, please have ready:
- Origin and destination (city/port)
- Cargo description and HS code (if known)
- Total weight and dimensions
- Desired shipping mode (sea/air)
- Preferred timeline
- Any special requirements (temperature control, hazardous, etc.)

## Step 2: Submit Quote Request
You can request a quote by:
- Using our online quote form [link if available]
- Emailing sales@tigerlogistics.com
- Calling +1-XXX-XXX-XXXX

## Step 3: Quote Review (1-2 Business Days)
Our team will:
- Review your requirements
- Confirm feasibility
- Calculate pricing
- Send detailed quote via email

## Step 4: Booking Confirmation
Once you accept the quote:
- Reply to confirm acceptance
- Provide booking details and documents
- We'll reserve space and send booking confirmation

## Step 5: Shipment Execution
Your dedicated account manager will coordinate all logistics.
```

---

## QUALITY CHECKLIST

Before adding a document to the knowledge base, verify:

- [ ] Information is current and accurate
- [ ] Tone is neutral and professional
- [ ] No promises that can't be kept (e.g., "guaranteed 5-day delivery")
- [ ] No specific prices (unless approved and static)
- [ ] Contact info is centralized and current
- [ ] No typos or grammar errors
- [ ] Headers and structure are clear
- [ ] Examples are concrete, not vague
- [ ] File is properly named and in correct bucket
- [ ] No confidential or sensitive data

---

## DOCUMENT PRIORITY (FOR MVP)

### High Priority (Must Have)
1. Customer FAQ (most common 10-15 questions)
2. Service descriptions (sea freight, air cargo, customs)
3. How to get a quote
4. Basic documentation requirements

### Medium Priority (Should Have)
5. Service geographic coverage
6. Pricing structure overview (no exact prices)
7. Payment and contract terms
8. Tracking process explanation

### Low Priority (Nice to Have)
9. Detailed internal procedures
10. Advanced service options
11. Industry terminology glossary

---

## INITIAL 20-PAGE RECOMMENDATION

**Start with these 20 documents:**

**Customer Support (8 files):**
1. General FAQ
2. Shipping documentation guide
3. Tracking instructions
4. Claims process
5. Sea freight FAQ
6. Air cargo FAQ
7. Customs clearance FAQ
8. Contact information

**Services & Pricing (6 files):**
9. Sea freight services overview
10. Air cargo services overview
11. Customs brokerage services
12. Additional services (warehousing, insurance, etc.)
13. Service coverage areas
14. Pricing structure explanation (no exact prices)

**Sales Process (4 files):**
15. How to request a quote
16. Onboarding process
17. Required customer information
18. Payment terms and conditions

**Internal (2 files):**
19. Escalation procedures
20. Quality standards

---

## ONGOING MAINTENANCE

### Monthly Review
- Check for outdated information
- Add commonly asked questions that aren't covered
- Remove deprecated policies

### After Each Update
- Test bot with new/changed content
- Verify no hallucinations introduced
- Check response quality

### Expansion Strategy
- Start with 20 pages
- Add 5-10 pages per month based on:
  - Questions bot can't answer
  - New services launched
  - Customer feedback

---

## TOOLS & FORMAT TIPS

**Recommended editors:**
- VS Code with Markdown preview
- Obsidian (for linking between docs)
- Notion (if team collaboration needed)

**File naming convention:**
- Use lowercase
- Use underscores not spaces
- Use descriptive names: `sea_freight_faq.md` not `doc1.md`
- Prefix with numbers if order matters: `01_intro.md`, `02_services.md`

**Character encoding:**
- UTF-8 always
- Avoid special characters in filenames

---

## WHAT TO DO NEXT

1. **Audit existing content:** Gather any existing FAQs, service descriptions, or internal docs
2. **Identify gaps:** List what's missing from the 20 recommended files
3. **Create drafts:** Start with rough content—perfection comes later
4. **Review with stakeholders:** Get management/sales/ops input on accuracy
5. **Format consistently:** Use the templates above
6. **Stage for ingestion:** Place in correct bucket folders

**Timeline:** Aim to have 15-20 documents ready before starting backend build.

---

## QUESTIONS TO ASK STAKEHOLDERS

Before finalizing documents:

**To Management:**
- What information should NOT be in the knowledge base?
- Who needs to approve content before it goes live?

**To Sales Team:**
- What questions do customers ask most often?
- What information do you wish was easier to share?

**To Operations:**
- What are the most common misunderstandings customers have?
- What processes are most confusing to explain?

**To Customer Service:**
- What are the top 10 tickets you handle?
- Which answers do you copy-paste most often?

---

**Next step:** Start gathering and creating these documents. Quality over quantity for MVP.