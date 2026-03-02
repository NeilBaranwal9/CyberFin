import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
from collections import defaultdict
import community.community_louvain as community_louvain

class CyberFinDetector:
    def __init__(self, cyber_df, txn_df):
        self.cyber_df = cyber_df
        self.txn_df = txn_df
        self.cyber_df['timestamp'] = pd.to_datetime(self.cyber_df['timestamp'])
        self.txn_df['timestamp'] = pd.to_datetime(self.txn_df['timestamp'])
        self.graph = nx.Graph()
        self.risk_scores = {}
        
    def build_graph(self):
        """Build network graph connecting accounts, devices, IPs, and beneficiaries"""
        # Add account-device edges
        for _, row in self.cyber_df.iterrows():
            self.graph.add_edge(row['account_id'], f"DEV_{row['device']}", type='device')
            self.graph.add_edge(row['account_id'], f"IP_{row['ip']}", type='ip')
        
        # Add account-beneficiary edges
        for _, row in self.txn_df.iterrows():
            self.graph.add_edge(row['account_id'], row['beneficiary'], 
                              type='transaction', amount=row['amount'])
        
        print(f"✅ Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        
    def detect_cyber_anomalies(self, account_id, time_window_minutes=60):
        """Detect suspicious cyber activity patterns"""
        recent_time = datetime.now() - timedelta(minutes=time_window_minutes)
        account_events = self.cyber_df[
            (self.cyber_df['account_id'] == account_id) & 
            (self.cyber_df['timestamp'] >= recent_time)
        ]
        
        flags = []
        if len(account_events[account_events['event_type'] == 'malware_signal']) > 0:
            flags.append('malware_detected')
        if len(account_events[account_events['event_type'] == 'new_device']) > 0:
            flags.append('new_device')
        if len(account_events[account_events['event_type'] == 'foreign_ip']) > 0:
            flags.append('foreign_ip')
        if len(account_events[account_events['event_type'] == 'password_reset']) > 0:
            flags.append('password_reset')
        if len(account_events[account_events['event_type'] == 'login_fail']) >= 3:
            flags.append('multiple_login_failures')
            
        return flags
    
    def detect_financial_velocity(self, account_id, time_window_minutes=120):
        """Detect rapid/high-value transactions"""
        recent_time = datetime.now() - timedelta(minutes=time_window_minutes)
        account_txns = self.txn_df[
            (self.txn_df['account_id'] == account_id) & 
            (self.txn_df['timestamp'] >= recent_time)
        ]
        
        flags = []
        if len(account_txns) >= 3:
            flags.append('rapid_transactions')
        if (account_txns['amount'] > 45000).any():
            flags.append('near_threshold_amount')
        if account_txns['amount'].sum() > 100000:
            flags.append('high_total_volume')
            
        return flags
    
    def detect_mule_rings(self):
        """Detect connected mule networks using community detection"""
        # Find communities (rings) in the graph
        communities = community_louvain.best_partition(self.graph)
        
        # Group accounts by community
        community_accounts = defaultdict(list)
        for node, comm_id in communities.items():
            if node.startswith('ACC_'):
                community_accounts[comm_id].append(node)
        
        # Flag suspicious communities (multiple accounts sharing beneficiaries)
        suspicious_rings = []
        for comm_id, accounts in community_accounts.items():
            if len(accounts) >= 3:  # At least 3 accounts in ring
                # Check if they share beneficiaries
                shared_beneficiaries = set()
                for acc in accounts:
                    neighbors = list(self.graph.neighbors(acc))
                    beneficiaries = [n for n in neighbors if n.startswith('BEN_')]
                    shared_beneficiaries.update(beneficiaries)
                
                if len(shared_beneficiaries) > 0:
                    suspicious_rings.append({
                        'ring_id': comm_id,
                        'accounts': accounts,
                        'shared_beneficiaries': list(shared_beneficiaries),
                        'size': len(accounts)
                    })
        
        return suspicious_rings
    
    def calculate_risk_score(self, account_id):
        """Calculate composite risk score (0-100)"""
        score = 0
        
        # Cyber anomaly score (40 points max)
        cyber_flags = self.detect_cyber_anomalies(account_id)
        score += len(cyber_flags) * 10
        
        # Financial velocity score (30 points max)
        fin_flags = self.detect_financial_velocity(account_id)
        score += len(fin_flags) * 10
        
        # Network centrality score (30 points max)
        if account_id in self.graph:
            degree = self.graph.degree(account_id)
            score += min(degree * 2, 30)
        
        self.risk_scores[account_id] = min(score, 100)
        return self.risk_scores[account_id]
    
    def get_flagged_accounts(self, threshold=50):
        """Get all accounts above risk threshold"""
        flagged = []
        for account in self.cyber_df['account_id'].unique():
            score = self.calculate_risk_score(account)
            if score >= threshold:
                flagged.append({
                    'account_id': account,
                    'risk_score': score,
                    'cyber_flags': self.detect_cyber_anomalies(account),
                    'financial_flags': self.detect_financial_velocity(account)
                })
        
        return sorted(flagged, key=lambda x: x['risk_score'], reverse=True)

if __name__ == "__main__":
    # Test the detector
    cyber = pd.read_csv('cyber_events.csv')
    txns = pd.read_csv('transactions.csv')
    
    detector = CyberFinDetector(cyber, txns)
    detector.build_graph()
    
    print("\n🔍 Detecting mule rings...")
    rings = detector.detect_mule_rings()
    print(f"Found {len(rings)} suspicious rings")
    for ring in rings[:3]:
        print(f"  Ring {ring['ring_id']}: {ring['size']} accounts → {ring['shared_beneficiaries']}")
    
    print("\n⚠️  Top 10 high-risk accounts:")
    flagged = detector.get_flagged_accounts(threshold=40)
    for acc in flagged[:10]:
        print(f"  {acc['account_id']}: Risk={acc['risk_score']} | {acc['cyber_flags']} | {acc['financial_flags']}")
