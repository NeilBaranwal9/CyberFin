# 🛡️ CyberFin Fusion

**Stop the Money Before It Disappears**

Unified Cyber-Financial Intelligence Platform for detecting money mule networks in real-time.

## 🚀 Quick Start (24-Hour Hackathon)

### Phase 1: Setup (Complete ✅)
```bash
pip install -r requirements.txt
python data_generator.py
```

### Phase 2: Run Detection Engine
```bash
python detection_engine.py
```

### Phase 3: Launch Dashboard
```bash
streamlit run dashboard.py
```

### Phase 4: Start API (Optional)
```bash
python api.py
```

### Phase 5: Enable Gemini Explainability
1. Get API key from https://makersuite.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Add your key: `GEMINI_API_KEY=your_key`
4. Test: `python gemini_explainer.py`

## 📊 What We Built

- **20,000 realistic cyber events** + **2,400+ transactions**
- **Graph-based mule ring detection** using Louvain community detection
- **Real-time risk scoring** combining cyber + financial signals
- **Interactive dashboard** with live network visualization
- **AI-powered explanations** via Gemini (natural language insights)

## 🎯 Key Features

1. **Unified Intelligence**: Breaks down cyber/AML silos
2. **Pre-Transaction Alerts**: Stops money before it moves
3. **Network Detection**: Reveals hidden mule rings
4. **Explainable AI**: Human-readable risk explanations

## 📈 Detection Rules

### Cyber Anomalies
- Malware signals
- New device + foreign IP
- Password resets
- Multiple login failures

### Financial Velocity
- Rapid transactions (3+ in 2 hours)
- Near-threshold amounts (₹45k-₹49k)
- High total volume (>₹1L)

### Network Patterns
- Shared beneficiaries across accounts
- Community detection (Louvain algorithm)
- Graph centrality scoring

## 🏆 Why This Wins

Directly addresses the 4 problems from the infographic:
1. ✅ Cyber attacks fuel laundering → We ingest both streams
2. ✅ Silos → Unified platform
3. ✅ Mules look legitimate → Graph reveals rings
4. ✅ Detection too late → Real-time pre-transaction alerts

## 📁 Project Structure

```
CyberFin/
├── data_generator.py      # Mock data (20k events)
├── detection_engine.py    # Core detection logic
├── dashboard.py           # Streamlit UI
├── api.py                 # FastAPI backend
├── gemini_explainer.py    # AI explanations
├── cyber_events.csv       # Generated data
├── transactions.csv       # Generated data
└── requirements.txt       # Dependencies
```

## 🎤 Demo Script

1. Show "traditional view" (isolated events look normal)
2. Switch to "Fusion view" → rings appear
3. Click flagged account → Gemini explains the pattern
4. Show "Pause Transaction" button
5. Export SAR report

## 📊 Impact Numbers (For PPT)

- **India**: 19 lakh mule accounts (Jan 2026)
- **Losses**: ₹21,367 crore (H1 FY25)
- **Gen Z**: 35% would move money for fee (Barclays 2025)
- **Awareness**: 71% unaware of criminal consequences

## 🔮 Future Enhancements

- Real Kafka streaming
- Neo4j graph database
- ML-based anomaly detection
- Mobile app for alerts
- Blockchain tracing integration

---

**Built in 24 hours for [Hackathon Name]**
