# 🛡️ CyberFin - Money Mule Detection System

**Stop money laundering by detecting suspicious account networks in real-time.**

![Status](https://img.shields.io/badge/Status-Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10+-blue)

---

## 🎯 What Does This Do?

CyberFin detects "money mules" - people (often victims) whose bank accounts are used to launder money. It combines:
- Cyber security events (logins, malware, IP changes)
- Financial transactions (amounts, timing, beneficiaries)
- AI analysis to explain suspicious patterns

**Real Impact:** India identified 19 lakh mule accounts in 2025-2026, with ₹21,367 crore lost.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Python

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer, check "Add Python to PATH"
3. Click "Install Now"

**Mac:** `brew install python`

**Linux:** `sudo apt install python3 python3-pip`

### Step 2: Install & Setup

Open terminal in the `CyberFin` folder:

```bash
# Install dependencies (takes 2 minutes)
pip install -r requirements.txt

# Generate sample data (takes 5 seconds)
python data_generator.py
```

### Step 3: Launch Dashboard

```bash
streamlit run dashboard_enhanced.py
```

**Or on Windows, double-click:** `run_dashboard_enhanced.bat`

Dashboard opens automatically at http://localhost:8501

**That's it! You're running CyberFin.** 🎉

---

## 📖 How to Use

### Main Features

**1. Dashboard View** (Default)
- See all high-risk accounts
- View detected mule rings
- Export compliance reports

**2. Account Lookup**
- Enter account ID (try `ACC_002747`)
- See risk score and flags
- Get AI explanation
- Freeze account if needed

**3. Ring Analysis**
- View detected mule networks
- See all connected accounts
- Get AI explanation of patterns

**4. Live Graph**
- Visualize account connections
- See network relationships
- Interactive exploration

### Quick Actions

**Analyze an Account:**
1. Click "Account Lookup" at top
2. Enter: `ACC_002747`
3. Click "Analyze"
4. View risk score (0-100)
5. Read AI explanation

**View a Mule Ring:**
1. Click "Ring Analysis" at top
2. Select any ring from dropdown
3. Click "🤖 Generate AI Explanation"
4. See how the network operates

**Export Report:**
1. Click "📄 Generate SAR Report" in sidebar
2. Click "⬇️ Download SAR Report"
3. Get professional CSV report

---

## 🎮 Try These Examples

**High-Risk Accounts to Test:**
- `ACC_002747` - Risk: 90/100 (malware + rapid transactions)
- `ACC_004611` - Risk: 90/100 (foreign IP + structuring)
- `ACC_000815` - Risk: 88/100 (multiple devices)

**Interesting Rings:**
- Ring 13 - 23 accounts sharing beneficiaries
- Ring 0 - 479 accounts (largest network)

---

## 🔧 Troubleshooting

**Dashboard won't start?**
```bash
pip install streamlit
streamlit run dashboard_enhanced.py
```

**No data files?**
```bash
python data_generator.py
```

**Port already in use?**
```bash
streamlit run dashboard_enhanced.py --server.port 8502
```

**Import errors?**
```bash
pip install -r requirements.txt
```

---

## 🤖 Optional: Enable AI Features

CyberFin works without AI, but for enhanced explanations:

1. Get free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create `.env` file in CyberFin folder:
```
GEMINI_API_KEY=your_key_here
```
3. Restart dashboard

**Without API key:** System uses smart fallback mode (still works great!)

---

## 📊 What You'll See

**Dashboard Metrics:**
- Total accounts monitored
- High-risk accounts detected
- Mule rings identified
- Blocked transactions

**Risk Levels:**
- 🟢 0-49: Low Risk
- 🟡 50-69: High Risk (review needed)
- 🔴 70-100: Critical Risk (freeze recommended)

**AI Explanations:**
- Why account is suspicious
- How victim was likely recruited
- Recommended actions
- Investigation steps

---

## 📁 Key Files

```
CyberFin/
├── dashboard_enhanced.py      # Main dashboard (run this!)
├── data_generator.py          # Creates sample data
├── detection_engine.py        # Risk detection logic
├── backend.py                 # API server (optional)
├── requirements.txt           # Dependencies
├── cyber_events.csv           # Generated data
└── a_transactions.csv         # Generated data
```

---

## 🧪 Testing

Verify everything works:

```bash
pytest tests/ -v -m "not slow"
```

Expected: ✅ 52 tests passed

---

## 💻 System Requirements

- **Python:** 3.10 or higher
- **RAM:** 4GB minimum
- **Disk:** 500MB free space
- **OS:** Windows, Mac, or Linux
- **Internet:** For initial setup only

---

## 🎓 Understanding the System

**What are money mules?**
People whose bank accounts are used to transfer illegal money. Often victims recruited through fake job offers.

**How does detection work?**
1. Analyzes cyber events (malware, suspicious logins)
2. Tracks financial transactions (amounts, timing)
3. Builds network graph (who's connected to whom)
4. Calculates risk scores (0-100)
5. Identifies mule rings (groups working together)

**Why is this important?**
- Stops money laundering
- Protects victims
- Helps compliance teams
- Prevents financial crime

---

## 🚀 Advanced Usage

### Run Backend API (Optional)

```bash
python backend.py
```

API docs: http://localhost:8000/docs

### Run Tests

```bash
# Quick tests
pytest tests/ -v -m "not slow"

# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Use Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Additional Documentation

- `DEMO_CHEAT_SHEET.txt` - Quick demo guide
- `TESTING_GUIDE.md` - Testing details
- `AI_FEATURES_GUIDE.md` - AI setup guide
- `GNN_INTEGRATION_COMPLETE.md` - AI model details

---

## 🎯 Quick Commands

```bash
# Generate data
python data_generator.py

# Run dashboard
streamlit run dashboard_enhanced.py

# Run backend (optional)
python backend.py

# Run tests
pytest tests/ -v -m "not slow"
```

---

## 🆘 Need Help?

1. **Check troubleshooting section above**
2. **Regenerate data:** `python data_generator.py`
3. **Reinstall dependencies:** `pip install -r requirements.txt`
4. **Use different port:** `streamlit run dashboard_enhanced.py --server.port 8502`

---

## 🏆 Features

✅ Real-time risk detection  
✅ AI-powered explanations  
✅ Network visualization  
✅ Compliance reporting  
✅ One-click account freezing  
✅ Victim education scenarios  
✅ Professional SAR exports  
✅ 66 automated tests  

---

## 📞 Support

**Common Issues:**
- Dashboard won't start → Install streamlit
- No data → Run data_generator.py
- Import errors → Run pip install -r requirements.txt
- Port in use → Use different port (8502)

---

**Built for detecting financial crime and protecting victims** 🛡️

*CyberFin - Stop the Money Before It Disappears*
