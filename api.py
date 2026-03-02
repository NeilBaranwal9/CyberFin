from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from detection_engine import CyberFinDetector
from pydantic import BaseModel

app = FastAPI(title="CyberFin Fusion API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data and detector
cyber_df = pd.read_csv('cyber_events.csv')
txn_df = pd.read_csv('transactions.csv')
detector = CyberFinDetector(cyber_df, txn_df)
detector.build_graph()

class AccountRequest(BaseModel):
    account_id: str

@app.get("/")
def root():
    return {"message": "CyberFin Fusion API", "status": "active"}

@app.get("/stats")
def get_stats():
    return {
        "total_events": len(cyber_df),
        "total_transactions": len(txn_df),
        "total_accounts": cyber_df['account_id'].nunique(),
        "graph_nodes": detector.graph.number_of_nodes(),
        "graph_edges": detector.graph.number_of_edges()
    }

@app.get("/flagged/{threshold}")
def get_flagged_accounts(threshold: int = 50):
    flagged = detector.get_flagged_accounts(threshold=threshold)
    return {"count": len(flagged), "accounts": flagged[:50]}

@app.get("/rings")
def get_mule_rings():
    rings = detector.detect_mule_rings()
    return {"count": len(rings), "rings": rings[:20]}

@app.post("/analyze")
def analyze_account(request: AccountRequest):
    account_id = request.account_id
    
    if account_id not in cyber_df['account_id'].values:
        raise HTTPException(status_code=404, detail="Account not found")
    
    risk_score = detector.calculate_risk_score(account_id)
    cyber_flags = detector.detect_cyber_anomalies(account_id)
    fin_flags = detector.detect_financial_velocity(account_id)
    
    return {
        "account_id": account_id,
        "risk_score": risk_score,
        "cyber_flags": cyber_flags,
        "financial_flags": fin_flags,
        "status": "critical" if risk_score >= 70 else "high" if risk_score >= 50 else "low"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
