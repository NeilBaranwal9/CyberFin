# Risk Assessment Flow with GNN Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CyberFin System                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
├─────────────────────────────────────────────────────────────┤
│  • cyber_events.csv  (IP, Device, Location data)           │
│  • a_transactions.csv (Transaction history)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              GNN Risk Scorer (NEW)                           │
├─────────────────────────────────────────────────────────────┤
│  1. Extract Features (7 per account)                        │
│  2. Build k-NN Graph                                        │
│  3. Load Trained Model (best_gnn_a_transactions.pth)       │
│  4. Generate Risk Scores (0-100)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           Detection Engine (ENHANCED)                        │
├─────────────────────────────────────────────────────────────┤
│  calculate_risk_score(account_id):                          │
│                                                              │
│  ┌─────────────────────────────────────────┐               │
│  │ Is GNN Available?                        │               │
│  └─────────────────────────────────────────┘               │
│           │                    │                             │
│          YES                  NO                             │
│           │                    │                             │
│           ▼                    ▼                             │
│  ┌──────────────┐    ┌──────────────────┐                  │
│  │ GNN Scoring  │    │ Rule-Based Only  │                  │
│  ├──────────────┤    ├──────────────────┤                  │
│  │ Base: GNN    │    │ Cyber: 10pts ea  │                  │
│  │ + Cyber: 5pt │    │ Finance: 10pts   │                  │
│  │ + Finance:5pt│    │ Network: 30pts   │                  │
│  └──────────────┘    └──────────────────┘                  │
│           │                    │                             │
│           └────────┬───────────┘                             │
│                    ▼                                         │
│           Final Risk Score (0-100)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Risk Classification                             │
├─────────────────────────────────────────────────────────────┤
│  • 0-49:   LOW RISK      ✅ Monitor normally                │
│  • 50-69:  HIGH RISK     ⚠️  Flag for review                │
│  • 70-100: CRITICAL RISK 🚨 Recommend freeze                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Backend API Response                          │
├─────────────────────────────────────────────────────────────┤
│  {                                                           │
│    "account_id": "ACC_001",                                 │
│    "risk_score": 75,                                        │
│    "risk_bucket": "critical",                               │
│    "status": "ACTIVE",                                      │
│    "cyber_flags": [...],                                    │
│    "financial_flags": [...]                                 │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  UI Display                                  │
├─────────────────────────────────────────────────────────────┤
│  Risk Score: 75/100                                         │
│  🧠 AI-Enhanced Scoring Active  ← NEW INDICATOR             │
│  Status: 🔴 ACTIVE                                          │
│  🚨 CRITICAL RISK DETECTED                                  │
│                                                              │
│  [🛑 Freeze Account]  [📋 Download SAR]                     │
└─────────────────────────────────────────────────────────────┘
```

## Feature Extraction for GNN

```
For each account:
┌────────────────────────────────────────┐
│ Feature Vector (7 dimensions)          │
├────────────────────────────────────────┤
│ 1. Cyber event count                   │
│ 2. Unique IP addresses                 │
│ 3. Unique device IDs                   │
│ 4. Transaction count                   │
│ 5. Total transaction amount            │
│ 6. Average transaction amount          │
│ 7. Unique beneficiaries                │
└────────────────────────────────────────┘
         │
         ▼
   Standardized
         │
         ▼
   k-NN Graph (k=5)
         │
         ▼
   GNN Model
         │
         ▼
   Risk Probability
```

## Risk Score Comparison

### Example Account: ACC_001

**Scenario 1: GNN Available**
```
GNN Base Score:           65.0
+ Cyber Anomalies (2):   +10.0  (2 × 5)
+ Financial Flags (1):    +5.0  (1 × 5)
─────────────────────────────
Final Risk Score:         80.0  🚨 CRITICAL
```

**Scenario 2: GNN Unavailable (Fallback)**
```
Cyber Anomalies (2):      20.0  (2 × 10)
Financial Flags (1):      10.0  (1 × 10)
Network Centrality:       24.0  (degree × 2)
─────────────────────────────
Final Risk Score:         54.0  ⚠️ HIGH
```

**Key Difference**: GNN captures learned patterns that rules might miss

## Decision Flow

```
Risk Score Calculated
        │
        ▼
   ┌─────────┐
   │ ≥ 70?   │──YES──▶ 🚨 CRITICAL
   └─────────┘           │
        │NO              ▼
        ▼           Recommend Freeze
   ┌─────────┐     Generate SAR
   │ ≥ 50?   │──YES──▶ ⚠️ HIGH
   └─────────┘           │
        │NO              ▼
        ▼           Flag for Review
   ✅ LOW              │
        │               │
        ▼               ▼
   Monitor         Update Status
```

## Integration Points

1. **Backend Startup**: Initialize GNN scorer
2. **Risk Calculation**: Use GNN + rules
3. **API Response**: Include risk_score and risk_bucket
4. **UI Display**: Show AI indicator when GNN active
5. **Stats Endpoint**: Report GNN status

## Performance Considerations

- **GNN Inference**: ~10ms per account
- **Batch Scoring**: All accounts scored at startup
- **Caching**: Results cached for 60 seconds
- **Fallback**: Instant switch to rule-based if GNN fails

## Monitoring

Check GNN status:
```bash
curl http://localhost:8000/stats | jq '.gnn_enabled'
```

Expected output:
```json
{
  "gnn_enabled": true,
  ...
}
```
