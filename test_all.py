"""
Quick test script to verify all components work
"""
import pandas as pd
from detection_engine import CyberFinDetector
from gemini_explainer import GeminiExplainer

print("🧪 Testing CyberFin Fusion Components...\n")

# Test 1: Data loading
print("1️⃣ Testing data loading...")
try:
    cyber = pd.read_csv('cyber_events.csv')
    txns = pd.read_csv('transactions.csv')
    print(f"   ✅ Loaded {len(cyber)} cyber events")
    print(f"   ✅ Loaded {len(txns)} transactions\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

# Test 2: Detection engine
print("2️⃣ Testing detection engine...")
try:
    detector = CyberFinDetector(cyber, txns)
    detector.build_graph()
    print(f"   ✅ Graph built: {detector.graph.number_of_nodes()} nodes\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

# Test 3: Mule ring detection
print("3️⃣ Testing mule ring detection...")
try:
    rings = detector.detect_mule_rings()
    print(f"   ✅ Found {len(rings)} suspicious rings")
    if rings:
        print(f"   📊 Largest ring: {rings[0]['size']} accounts\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

# Test 4: Risk scoring
print("4️⃣ Testing risk scoring...")
try:
    flagged = detector.get_flagged_accounts(threshold=50)
    print(f"   ✅ Found {len(flagged)} high-risk accounts")
    if flagged:
        top = flagged[0]
        print(f"   🚨 Highest risk: {top['account_id']} (Score: {top['risk_score']})\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

# Test 5: Gemini explainer
print("5️⃣ Testing Gemini explainer...")
try:
    explainer = GeminiExplainer()
    if flagged:
        test_acc = flagged[0]
        explanation = explainer.explain_mule_pattern(
            {'account_id': test_acc['account_id'], 'risk_score': test_acc['risk_score']},
            test_acc['cyber_flags'],
            test_acc['financial_flags']
        )
        print(f"   ✅ Generated explanation ({len(explanation)} chars)\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n🚀 Ready to launch:")
print("   • Dashboard: streamlit run dashboard.py")
print("   • API: python api.py")
print("\n📊 Quick Stats:")
print(f"   • Total Events: {len(cyber):,}")
print(f"   • Total Transactions: {len(txns):,}")
print(f"   • Mule Rings: {len(rings)}")
print(f"   • High-Risk Accounts: {len(flagged)}")
print(f"   • Graph Nodes: {detector.graph.number_of_nodes():,}")
print(f"   • Graph Edges: {detector.graph.number_of_edges():,}")
