"""
GNN-based Risk Scoring Module
Integrates trained GNN model for account risk assessment
"""
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
from typing import Dict, Optional


class PureGCNLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super(PureGCNLayer, self).__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x, edge_index):
        num_nodes = x.size(0)
        
        # Create Adjacency Matrix
        adj = torch.zeros((num_nodes, num_nodes), device=x.device)
        adj[edge_index[0], edge_index[1]] = 1.0
        
        # Add self-loops
        adj += torch.eye(num_nodes, device=x.device)
        
        # Normalize
        deg = adj.sum(dim=1, keepdim=True)
        adj_norm = adj / deg
        
        # Message Passing
        aggregated_features = torch.matmul(adj_norm, x)
        
        return self.linear(aggregated_features)


class MuleGNN(nn.Module):
    def __init__(self, input_dim):
        super(MuleGNN, self).__init__()
        self.conv1 = PureGCNLayer(input_dim, 64)
        self.conv2 = PureGCNLayer(64, 32)
        
        self.fc1 = nn.Linear(32, 16)
        self.fc2 = nn.Linear(16, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index):
        x = self.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv2(x, edge_index))
        
        x = self.relu(self.fc1(x))
        out = self.fc2(x)
        return out


class GNNRiskScorer:
    """
    Loads trained GNN model and provides risk scoring for accounts
    """
    def __init__(self, model_path: str = "best_gnn_a_transactions.pth"):
        self.model_path = model_path
        self.model: Optional[MuleGNN] = None
        self.scaler = StandardScaler()
        self.account_to_idx: Dict[str, int] = {}
        self.idx_to_account: Dict[int, str] = {}
        self.is_loaded = False
        
    def load_model(self, cyber_df: pd.DataFrame, txn_df: pd.DataFrame):
        """
        Load GNN model and prepare data structures
        """
        try:
            # Prepare features from transaction data
            features = self._extract_features(cyber_df, txn_df)
            
            if features is None or len(features) == 0:
                print("⚠️ GNN: No features extracted, using fallback scoring")
                return False
            
            # Create account mapping
            accounts = list(features.keys())
            self.account_to_idx = {acc: idx for idx, acc in enumerate(accounts)}
            self.idx_to_account = {idx: acc for acc, idx in self.account_to_idx.items()}
            
            # Prepare feature matrix
            feature_matrix = np.array([features[acc] for acc in accounts])
            self.feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
            
            # Build k-NN graph
            self.edge_index = self._build_knn_graph(self.feature_matrix_scaled, k=5)
            
            # Convert to tensors
            self.x_tensor = torch.tensor(self.feature_matrix_scaled, dtype=torch.float32)
            
            # Initialize and load model
            input_dim = self.x_tensor.size(1)
            self.model = MuleGNN(input_dim)
            
            if os.path.exists(self.model_path):
                self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
                self.model.eval()
                self.is_loaded = True
                print(f"✅ GNN Model loaded from {self.model_path}")
                return True
            else:
                print(f"⚠️ GNN model file not found: {self.model_path}")
                return False
                
        except Exception as e:
            print(f"⚠️ GNN Model loading failed: {e}")
            return False
    
    def _extract_features(self, cyber_df: pd.DataFrame, txn_df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Extract features for each account from cyber and transaction data
        """
        features = {}
        
        for account_id in cyber_df['account_id'].unique():
            # Cyber features
            acc_cyber = cyber_df[cyber_df['account_id'] == account_id]
            
            # Transaction features
            acc_txns = txn_df[txn_df['from_account'] == account_id]
            
            feature_vec = [
                len(acc_cyber),  # Number of cyber events
                acc_cyber['ip_address'].nunique() if len(acc_cyber) > 0 else 0,  # Unique IPs
                acc_cyber['device_id'].nunique() if len(acc_cyber) > 0 else 0,  # Unique devices
                len(acc_txns),  # Number of transactions
                acc_txns['amount'].sum() if len(acc_txns) > 0 else 0,  # Total amount
                acc_txns['amount'].mean() if len(acc_txns) > 0 else 0,  # Avg amount
                acc_txns['to_account'].nunique() if len(acc_txns) > 0 else 0,  # Unique beneficiaries
            ]
            
            features[account_id] = np.array(feature_vec, dtype=np.float32)
        
        return features
    
    def _build_knn_graph(self, features: np.ndarray, k: int = 5) -> torch.Tensor:
        """
        Build k-NN graph from feature matrix
        """
        x_tensor = torch.tensor(features, dtype=torch.float32)
        dist = torch.cdist(x_tensor, x_tensor)
        _, indices = dist.topk(k + 1, dim=1, largest=False)
        neighbors = indices[:, 1:]
        
        src = torch.arange(x_tensor.size(0)).view(-1, 1).repeat(1, k).view(-1)
        dst = neighbors.reshape(-1)
        
        return torch.stack([src, dst], dim=0)
    
    def get_gnn_risk_score(self, account_id: str) -> float:
        """
        Get GNN-based risk score for an account (0-100 scale)
        Returns -1 if model not loaded or account not found
        """
        if not self.is_loaded or self.model is None:
            return -1
        
        if account_id not in self.account_to_idx:
            return -1
        
        try:
            with torch.no_grad():
                # Get model prediction
                logits = self.model(self.x_tensor, self.edge_index)
                probs = torch.sigmoid(logits)
                
                # Get score for this account
                idx = self.account_to_idx[account_id]
                risk_prob = probs[idx].item()
                
                # Convert to 0-100 scale
                risk_score = risk_prob * 100
                
                return risk_score
                
        except Exception as e:
            print(f"⚠️ GNN scoring error for {account_id}: {e}")
            return -1
    
    def get_all_gnn_scores(self) -> Dict[str, float]:
        """
        Get GNN risk scores for all accounts
        """
        if not self.is_loaded or self.model is None:
            return {}
        
        try:
            with torch.no_grad():
                logits = self.model(self.x_tensor, self.edge_index)
                probs = torch.sigmoid(logits)
                
                scores = {}
                for account_id, idx in self.account_to_idx.items():
                    risk_prob = probs[idx].item()
                    scores[account_id] = risk_prob * 100
                
                return scores
                
        except Exception as e:
            print(f"⚠️ GNN batch scoring error: {e}")
            return {}


# Global instance
gnn_scorer: Optional[GNNRiskScorer] = None


def initialize_gnn_scorer(cyber_df: pd.DataFrame, txn_df: pd.DataFrame, model_path: str = "best_gnn_a_transactions.pth") -> bool:
    """
    Initialize the global GNN scorer
    """
    global gnn_scorer
    gnn_scorer = GNNRiskScorer(model_path)
    return gnn_scorer.load_model(cyber_df, txn_df)


def get_gnn_risk(account_id: str) -> float:
    """
    Get GNN risk score for an account
    Returns -1 if GNN not available
    """
    if gnn_scorer is None:
        return -1
    return gnn_scorer.get_gnn_risk_score(account_id)
