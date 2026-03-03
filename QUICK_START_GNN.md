# Quick Start: GNN-Enhanced Risk Scoring

## Installation

1. Install new dependencies:
```bash
pip install torch scikit-learn
```

2. Verify the GNN model file exists:
```bash
ls -lh best_gnn_a_transactions.pth
```

## Testing the Integration

Run the test script:
```bash
cd CyberFin
python test_gnn_integration.py
```

Expected output:
```
Loading data...
Loaded 1000 cyber events and 500 transactions

Initializing GNN scorer...
✅ GNN Model loaded from best_gnn_a_transactions.pth
✅ GNN scorer initialized successfully!

============================================================
Testing GNN Risk Scoring
============================================================

ACC_001:
  GNN Risk Score: 75.23/100
  Risk Level: CRITICAL
  🚨 CRITICAL - Consider freezing

ACC_002:
  GNN Risk Score: 42.15/100
  Risk Level: LOW

...

============================================================
Overall Statistics
============================================================
Total accounts scored: 100
Average risk score: 45.67
Max risk score: 89.34
Min risk score: 12.45

High risk accounts (≥50): 23 (23.0%)
Critical risk accounts (≥70): 8 (8.0%)
```

## Starting the System

1. Start the backend:
```bash
python backend.py
```

Look for this message:
```
✅ GNN Risk Scorer initialized successfully
```

2. Start the dashboard:
```bash
streamlit run dashboard_enhanced.py
```

## Verifying GNN is Active

### Method 1: Check API
```bash
curl http://localhost:8000/stats | jq '.gnn_enabled'
```

Should return: `true`

### Method 2: Check UI
1. Go to "Account Analysis" tab
2. Enter an account ID
3. Look for "🧠 AI-Enhanced Scoring Active" below the risk score

### Method 3: Check Logs
Backend startup should show:
```
✅ GNN Risk Scorer initialized successfully
```

## Understanding Risk Scores

### With GNN Active
- **Base Score**: From trained AI model
- **Adjustments**: Real-time anomaly detection
- **Result**: More accurate, learned from patterns

### Without GNN (Fallback)
- **Pure Rules**: Cyber flags + financial flags + network
- **Result**: Still functional, but less sophisticated

## Risk Thresholds

| Score | Level | Action | UI Indicator |
|-------|-------|--------|--------------|
| 0-49 | Low | Monitor | ✅ LOW RISK |
| 50-69 | High | Review | ⚠️ HIGH RISK |
| 70-100 | Critical | Freeze | 🚨 CRITICAL RISK |

## Troubleshooting

### GNN Not Loading

**Problem**: "⚠️ GNN Risk Scorer not available"

**Solutions**:
1. Check model file exists: `ls best_gnn_a_transactions.pth`
2. Install torch: `pip install torch`
3. Check data files: `ls cyber_events.csv a_transactions.csv`

### Import Errors

**Problem**: "ModuleNotFoundError: No module named 'torch'"

**Solution**:
```bash
pip install torch scikit-learn
```

### Model Loading Fails

**Problem**: Model file corrupted or incompatible

**Solution**: System automatically falls back to rule-based scoring. Check logs for details.

## Key Features

✅ **Automatic Fallback**: Works even if GNN unavailable
✅ **No UI Changes**: Existing interface preserved  
✅ **Performance**: Fast inference (~10ms per account)
✅ **Transparency**: Shows when AI is active
✅ **Hybrid Approach**: Combines AI + rules

## Files to Know

- `gnn_risk_scorer.py` - GNN model loader
- `best_gnn_a_transactions.pth` - Trained model weights
- `test_gnn_integration.py` - Integration test
- `GNN_INTEGRATION_COMPLETE.md` - Full documentation
- `RISK_ASSESSMENT_FLOW.md` - Architecture diagram

## API Changes

### `/stats` Endpoint
Now includes:
```json
{
  "gnn_enabled": true,
  ...
}
```

### `/account/{account_id}` Endpoint
No changes - risk_score now GNN-enhanced when available

## Next Steps

1. ✅ Install dependencies
2. ✅ Run test script
3. ✅ Start backend
4. ✅ Start dashboard
5. ✅ Verify "🧠 AI-Enhanced Scoring Active"
6. ✅ Test with sample accounts

## Support

If you encounter issues:
1. Check logs for error messages
2. Verify all dependencies installed
3. Ensure model file exists
4. System will fallback to rules if needed

The system is designed to work with or without GNN!
