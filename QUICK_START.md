# 🚀 CyberFin Fusion - Quick Start

## Launch Dashboard (Main Demo)
```bash
streamlit run dashboard.py
```
Or double-click: `run_dashboard.bat`

## What You'll See

### 1. Dashboard View
- 175 mule rings detected
- 283 high-risk accounts
- Event timeline
- Risk distribution

### 2. Live Graph View
- Select any ring
- Watch network visualization
- Red = accounts, Orange = beneficiaries

### 3. Account Lookup
- Try: `ACC_002747` (highest risk)
- See risk score: 90/100
- View AI explanation
- Test action buttons

## Key Demo Accounts

**Highest Risk:**
- ACC_002747 (Score: 90)
- ACC_004611 (Score: 90)
- ACC_000815 (Score: 88)

**Largest Ring:**
- Ring 0: 479 accounts

## Commands Cheat Sheet

```bash
# Generate new data
python data_generator.py

# Test everything
python test_all.py

# Run detection only
python detection_engine.py

# Start API
python api.py

# Launch dashboard
streamlit run dashboard.py
```

## Troubleshooting

**Dashboard won't start?**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

**No data?**
```bash
python data_generator.py
```

**Want Gemini AI?**
1. Get key: https://makersuite.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Add: `GEMINI_API_KEY=your_key`

## Demo Tips

1. Start with Dashboard view (impressive numbers)
2. Switch to Graph view (visual "wow")
3. Do Account Lookup (show AI explanation)
4. Click action buttons (show interactivity)
5. Total time: 3 minutes

## The "Aha!" Moment

When you show the graph view and the ring appears - that's when judges get it. The connections that are invisible in traditional systems become obvious.

---

**You're ready to demo! 🎯**
