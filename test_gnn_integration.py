"""
Test GNN Integration with Risk Scoring
"""
import pandas as pd
from gnn_risk_scorer import initialize_gnn_scorer, get_gnn_risk, gnn_scorer

# Load sample data
print("Loading data...")
cyber_df = pd.read_csv("cyber_events.csv")
txn_df = pd.read_csv("a_transactions.csv")

print(f"Loaded {len(cyber_df)} cyber events and {len(txn_df)} transactions")

# Initialize GNN scorer
print("\nInitializing GNN scorer...")
success = initialize_gnn_scorer(cyber_df, txn_df, "best_gnn_a_transactions.pth")

if success:
    print("✅ GNN scorer initialized successfully!")
    
    # Test scoring for a few accounts
    test_accounts = cyber_df['account_id'].unique()[:5]
    
    print("\n" + "="*60)
    print("Testing GNN Risk Scoring")
    print("="*60)
    
    for account_id in test_accounts:
        gnn_score = get_gnn_risk(account_id)
        
        if gnn_score >= 0:
            risk_level = "CRITICAL" if gnn_score >= 70 else "HIGH" if gnn_score >= 50 else "LOW"
            print(f"\n{account_id}:")
            print(f"  GNN Risk Score: {gnn_score:.2f}/100")
            print(f"  Risk Level: {risk_level}")
            
            # Show if account should be flagged
            if gnn_score >= 50:
                print(f"  ⚠️  FLAGGED - Requires review")
            if gnn_score >= 70:
                print(f"  🚨 CRITICAL - Consider freezing")
        else:
            print(f"\n{account_id}: GNN score not available")
    
    # Get all scores
    print("\n" + "="*60)
    print("Overall Statistics")
    print("="*60)
    
    all_scores = gnn_scorer.get_all_gnn_scores()
    if all_scores:
        scores_list = list(all_scores.values())
        print(f"Total accounts scored: {len(scores_list)}")
        print(f"Average risk score: {sum(scores_list)/len(scores_list):.2f}")
        print(f"Max risk score: {max(scores_list):.2f}")
        print(f"Min risk score: {min(scores_list):.2f}")
        
        high_risk = [s for s in scores_list if s >= 50]
        critical_risk = [s for s in scores_list if s >= 70]
        
        print(f"\nHigh risk accounts (≥50): {len(high_risk)} ({len(high_risk)/len(scores_list)*100:.1f}%)")
        print(f"Critical risk accounts (≥70): {len(critical_risk)} ({len(critical_risk)/len(scores_list)*100:.1f}%)")
        
else:
    print("❌ GNN scorer initialization failed")
    print("Falling back to rule-based scoring")

print("\n" + "="*60)
print("Test Complete")
print("="*60)
