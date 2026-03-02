import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from detection_engine import CyberFinDetector
from gemini_explainer import GeminiExplainer
import networkx as nx
from datetime import datetime

# Page config
st.set_page_config(page_title="CyberFin Fusion", layout="wide", page_icon="🛡️")

# Load data
@st.cache_data
def load_data():
    cyber = pd.read_csv('cyber_events.csv')
    txns = pd.read_csv('transactions.csv')
    return cyber, txns

@st.cache_resource
def initialize_detector(cyber, txns):
    detector = CyberFinDetector(cyber, txns)
    detector.build_graph()
    return detector

@st.cache_resource
def initialize_explainer():
    return GeminiExplainer()

# Main app
st.title("🛡️ CyberFin Fusion - Unified Cyber-Financial Intelligence")
st.markdown("**Stop the Money Before It Disappears**")

cyber_df, txn_df = load_data()
detector = initialize_detector(cyber_df, txn_df)
explainer = initialize_explainer()

# Sidebar
st.sidebar.header("⚙️ Controls")
risk_threshold = st.sidebar.slider("Risk Score Threshold", 0, 100, 50)
view_mode = st.sidebar.radio("View Mode", ["Dashboard", "Live Graph", "Account Lookup"])

if view_mode == "Dashboard":
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    flagged_accounts = detector.get_flagged_accounts(threshold=risk_threshold)
    rings = detector.detect_mule_rings()
    
    with col1:
        st.metric("🚨 Flagged Accounts", len(flagged_accounts))
    with col2:
        st.metric("🔗 Mule Rings Detected", len(rings))
    with col3:
        st.metric("📊 Total Events", len(cyber_df))
    with col4:
        st.metric("💰 Total Transactions", len(txn_df))
    
    # Top risks
    st.subheader("⚠️ High-Risk Accounts")
    if flagged_accounts:
        risk_data = []
        for acc in flagged_accounts[:20]:
            risk_data.append({
                'Account': acc['account_id'],
                'Risk Score': acc['risk_score'],
                'Cyber Flags': ', '.join(acc['cyber_flags']) if acc['cyber_flags'] else 'None',
                'Financial Flags': ', '.join(acc['financial_flags']) if acc['financial_flags'] else 'None'
            })
        
        df_risks = pd.DataFrame(risk_data)
        st.dataframe(df_risks, use_container_width=True)
        
        # Risk distribution
        fig_risk = px.histogram(df_risks, x='Risk Score', nbins=20, 
                               title="Risk Score Distribution",
                               color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Mule rings
    st.subheader("🔗 Detected Mule Rings")
    if rings:
        ring_data = []
        for ring in rings[:10]:
            ring_data.append({
                'Ring ID': ring['ring_id'],
                'Accounts': ring['size'],
                'Shared Beneficiaries': ', '.join(ring['shared_beneficiaries'])
            })
        
        df_rings = pd.DataFrame(ring_data)
        st.dataframe(df_rings, use_container_width=True)
    
    # Event timeline
    st.subheader("📈 Event Timeline")
    cyber_df['timestamp'] = pd.to_datetime(cyber_df['timestamp'])
    event_counts = cyber_df.groupby([pd.Grouper(key='timestamp', freq='1h'), 'event_type']).size().reset_index(name='count')
    
    fig_timeline = px.line(event_counts, x='timestamp', y='count', color='event_type',
                          title="Cyber Events Over Time")
    st.plotly_chart(fig_timeline, use_container_width=True)

elif view_mode == "Live Graph":
    st.subheader("🕸️ Network Graph Visualization")
    st.info("Showing connections between accounts, devices, IPs, and beneficiaries")
    
    # Select a ring to visualize
    rings = detector.detect_mule_rings()
    if rings:
        selected_ring = st.selectbox("Select Ring to Visualize", 
                                     [f"Ring {r['ring_id']} ({r['size']} accounts)" for r in rings[:10]])
        ring_idx = int(selected_ring.split()[1])
        
        ring = [r for r in rings if r['ring_id'] == ring_idx][0]
        
        # Create subgraph for this ring
        subgraph = nx.Graph()
        for acc in ring['accounts']:
            neighbors = list(detector.graph.neighbors(acc))
            for neighbor in neighbors:
                subgraph.add_edge(acc, neighbor)
        
        # Create plotly network graph
        pos = nx.spring_layout(subgraph, k=0.5, iterations=50)
        
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')
        
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
        
        node_trace = go.Scatter(
            x=[], y=[], text=[], mode='markers+text', hoverinfo='text',
            marker=dict(showscale=False, size=10, line_width=2))
        
        for node in subgraph.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node[:15]])
            
            # Color by type
            if node.startswith('ACC_'):
                node_trace['marker']['color'] = 'red'
            elif node.startswith('BEN_'):
                node_trace['marker']['color'] = 'orange'
            else:
                node_trace['marker']['color'] = 'lightblue'
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=f"Ring {ring_idx} Network",
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0,l=0,r=0,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write(f"**Accounts in Ring:** {', '.join(ring['accounts'][:10])}")
        st.write(f"**Shared Beneficiaries:** {', '.join(ring['shared_beneficiaries'])}")

elif view_mode == "Account Lookup":
    st.subheader("🔍 Account Risk Analysis")
    
    account_id = st.text_input("Enter Account ID (e.g., ACC_000860)")
    
    if account_id and st.button("Analyze"):
        if account_id in cyber_df['account_id'].values:
            risk_score = detector.calculate_risk_score(account_id)
            cyber_flags = detector.detect_cyber_anomalies(account_id)
            fin_flags = detector.detect_financial_velocity(account_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Risk Score", f"{risk_score}/100")
                
                if risk_score >= 70:
                    st.error("🚨 CRITICAL RISK")
                elif risk_score >= 50:
                    st.warning("⚠️ HIGH RISK")
                else:
                    st.success("✅ LOW RISK")
            
            with col2:
                st.write("**Cyber Flags:**")
                if cyber_flags:
                    for flag in cyber_flags:
                        st.write(f"- {flag}")
                else:
                    st.write("None")
                
                st.write("**Financial Flags:**")
                if fin_flags:
                    for flag in fin_flags:
                        st.write(f"- {flag}")
                else:
                    st.write("None")
            
            # Recent activity
            st.subheader("Recent Cyber Events")
            recent_cyber = cyber_df[cyber_df['account_id'] == account_id].tail(10)
            st.dataframe(recent_cyber, use_container_width=True)
            
            st.subheader("Recent Transactions")
            recent_txns = txn_df[txn_df['account_id'] == account_id].tail(10)
            if not recent_txns.empty:
                st.dataframe(recent_txns, use_container_width=True)
            else:
                st.info("No transactions found")
            
            # AI Explanation
            st.subheader("🤖 AI-Powered Explanation")
            with st.spinner("Generating explanation..."):
                account_data = {'account_id': account_id, 'risk_score': risk_score}
                explanation = explainer.explain_mule_pattern(account_data, cyber_flags, fin_flags)
                st.markdown(explanation)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛑 Freeze Account"):
                    st.success("Account frozen! Transaction blocked.")
            with col2:
                if st.button("📋 Generate SAR"):
                    st.success("SAR report generated!")
            with col3:
                if st.button("📞 Contact Customer"):
                    st.info("Alert sent to account holder")
        else:
            st.error("Account not found")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**CyberFin Fusion v1.0**")
st.sidebar.markdown("Built for 24hr Hackathon")
