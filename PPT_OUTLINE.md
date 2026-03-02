# CyberFin Fusion - Presentation Outline

## Slide 1: Title
**CyberFin Fusion**
*Stop the Money Before It Disappears*

Unified Cyber-Financial Intelligence Platform

Team: [Your Team Name]
Hackathon: [Event Name]

---

## Slide 2: The Problem (Use Infographic)
**4 Critical Failures in Current Systems:**

1. 🔴 Cyber attacks fuel money laundering
   - Phishing, malware, account takeovers recruit mules
   
2. 🔴 Cyber and AML systems operate in silos
   - No unified view of threats
   
3. 🔴 Mule accounts appear legitimate in isolation
   - Hidden networks invisible to single systems
   
4. 🔴 Detection happens too late
   - Money already gone when flagged

---

## Slide 3: Why People Become Mules (Root Causes)

**Economic Desperation + Awareness Gap**

📊 **Real Data (2025-2026):**
- 35% of Gen Z would move money for a stranger if offered a fee (Barclays 2025)
- 71% unaware it leads to criminal record (Barclays 2025)
- 30% of 18-24 year olds approached or know someone (Ireland 2025)

**How They're Recruited:**
- Fake "work from home" job offers (Instagram/WhatsApp)
- Romance scams
- "Easy money" promises (₹15k/week, zero risk)
- Targeting: Students, unemployed, financially stressed youth

---

## Slide 4: India Scale (2025-2026)

**The Crisis is Here:**

- 🚨 **19 lakh mule accounts** identified nationwide (MHA Jan 2026)
- 💰 **₹21,367 crore** lost in H1 FY25 alone (715% YoY jump)
- 🏦 **850,000+ accounts frozen** by banks (Nov 2025)
- 🤖 **RBI's MuleHunter.ai**: 20,000 mules/month, 23 banks adopted
- 📱 **13.42 lakh UPI fraud** incidents in FY23-24

**Current systems can't keep up.**

---

## Slide 5: The Missing Piece

**Traditional View:**
```
[Cyber System] ← Isolated → [AML System]
     ↓                           ↓
  Alerts                      Alerts
     ↓                           ↓
  Too Late                   Too Late
```

**What's Needed:**
```
[Cyber + Financial] → Unified Intelligence → Real-Time Action
```

**CyberFin Fusion = The Bridge**

---

## Slide 6: Our Solution

**CyberFin Fusion Platform**

✅ **Unified Intelligence Layer**
- Ingests cyber events + financial transactions in real-time
- Breaks down silos

✅ **Graph-Based Network Detection**
- Reveals hidden mule rings
- Community detection (Louvain algorithm)

✅ **Pre-Transaction Risk Scoring**
- Stops money before it moves
- Hybrid detection (cyber + financial + network)

✅ **AI-Powered Explanations**
- Gemini explains patterns in plain language
- Educates victims + regulators

---

## Slide 7: Architecture

```
┌─────────────────────────────────────────┐
│         Data Ingestion Layer            │
│  Cyber Events  │  Transactions          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│      Detection Engine (Python)          │
│  • Graph Builder (NetworkX)             │
│  • Anomaly Detection (Rules)            │
│  • Community Detection (Louvain)        │
│  • Risk Scoring (Hybrid)                │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Intelligence Layer                   │
│  • FastAPI Backend                      │
│  • Gemini Explainability                │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Presentation Layer                   │
│  • Streamlit Dashboard                  │
│  • Live Graph Visualization             │
│  • Real-Time Alerts                     │
└─────────────────────────────────────────┘
```

**Tech Stack:** Python, FastAPI, Streamlit, NetworkX, Plotly, Gemini AI

---

## Slide 8: Detection in Action (Screenshots)

**Before (Traditional View):**
- Individual events look normal
- No obvious patterns

**After (Fusion View):**
- 🔴 Red nodes light up
- Ring structure appears
- Shared beneficiaries visible

**Example:**
- 12 accounts
- All hit same 2 beneficiaries
- All show cyber compromise signals
- All transactions just under ₹50k threshold

---

## Slide 9: Detection Rules

**Cyber Anomalies (40 points):**
- Malware signals
- New device + foreign IP
- Password resets
- Multiple login failures

**Financial Velocity (30 points):**
- Rapid transactions (3+ in 2 hours)
- Near-threshold amounts (₹45k-₹49k)
- High total volume (>₹1L)

**Network Centrality (30 points):**
- Shared beneficiaries
- Community membership
- Graph degree

**Risk Score = 0-100 (Threshold: 50)**

---

## Slide 10: Gemini Explainability Demo

**Click any flagged account → AI explains:**

*"Account ACC_002747 compromised 47 min ago from Romania (malware-like behavior). Just sent ₹48,000 (just under threshold) to the same Singapore beneficiary that 4 other freshly-phished accounts also hit. Matches classic recruited-mule pattern targeting students in financial stress."*

**Why This Matters:**
- Educates investigators
- Speeds up decisions
- Explains to victims
- Regulatory compliance

---

## Slide 11: Live Demo

**Show:**
1. Dashboard overview (20k events, 173 rings detected)
2. High-risk accounts table
3. Network graph (ring visualization)
4. Account lookup → Risk analysis
5. Gemini explanation
6. Action buttons (Freeze, SAR, Contact)

**The "Aha!" Moment:**
- Watch the ring appear in real-time
- See connections invisible to traditional systems

---

## Slide 12: Impact & Future

**Immediate Impact:**
- ✅ Prevents losses (stops money before transfer)
- ✅ Protects victims (early intervention)
- ✅ Regulatory alignment (RBI, Europol, FATF)
- ✅ Scalable (works at bank/national level)

**Future Enhancements:**
- Real Kafka streaming (production-grade)
- Neo4j graph database (billions of nodes)
- ML-based anomaly detection (beyond rules)
- Mobile app for instant alerts
- Blockchain tracing integration

**This is what regulators have been demanding since 2023.**

---

## Slide 13: 24-Hour MVP Achievement

**What We Built:**
- ✅ 20,000 realistic mock events
- ✅ Graph-based detection engine
- ✅ Interactive dashboard
- ✅ FastAPI backend
- ✅ Gemini AI integration
- ✅ 173 mule rings detected
- ✅ Real-time risk scoring

**All functional, all demo-ready.**

---

## Slide 14: Why We Win

**We solved ALL 4 problems:**
1. ✅ Cyber fueling laundering → We ingest both
2. ✅ Silos → Unified platform
3. ✅ Mules look legitimate → Graph reveals rings
4. ✅ Too late → Pre-transaction alerts

**Plus:**
- Real-world data backing (India + global)
- Sponsor tech integration (Gemini)
- Production-ready architecture
- Regulatory alignment

**This isn't just a hackathon project. It's the solution.**

---

## Slide 15: Thank You

**CyberFin Fusion**
*We built what regulators have been begging for.*

**Team:** [Names]
**Contact:** [Email/GitHub]

**Try it:** [Demo Link if deployed]

**Questions?**

---

## Design Notes:
- Use dark green/teal theme (matches infographic)
- Include the infographic on Slide 2
- Use big numbers and icons
- Keep text minimal, visuals strong
- Screenshots from actual dashboard
- Network graph visualization is key visual

## Demo Tips:
1. Start with problem (infographic)
2. Show India numbers (shock value)
3. Live demo is the climax
4. End with "this is what they need"
5. Practice the "aha!" moment timing
