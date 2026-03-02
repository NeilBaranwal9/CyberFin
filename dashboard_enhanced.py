import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from detection_engine import CyberFinDetector
from gemini_explainer import GeminiExplainer
import networkx as nx
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(page_title="CyberFin Fusion", layout="wide", page_icon="🛡️")

# Demo mode warning
st.warning("⚠️ **DEMO MODE**: This system uses mock data for demonstration. Graph visualization limited to 500 nodes for performance. Production deployment would use real-time data streams and handle millions of nodes.", icon="⚠️")

# Custom CSS for better styling
st.markdown("""
<style>
    .victim-popup {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .alert-critical {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .demo-warning {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    cyber = pd.read_csv('cyber_events.csv')
    txns = pd.read_csv('transactions.csv')
    cyber['timestamp'] = pd.to_datetime(cyber['timestamp'])
    txns['timestamp'] = pd.to_datetime(txns['timestamp'])
    return cyber, txns

@st.cache_resource
def initialize_detector(cyber, txns):
    detector = CyberFinDetector(cyber, txns)
    detector.build_graph()
    return detector

@st.cache_resource
def initialize_explainer():
    explainer = GeminiExplainer()
    # Show API status in sidebar
    return explainer

# Fake job ads for victim popup
FAKE_JOB_ADS = [
    "💰 Earn ₹15,000/week from home! No experience needed. Just receive & transfer payments. Apply now!",
    "🏠 Work From Home - Payment Processing Agent. ₹20k/month guaranteed. Easy work, flexible hours!",
    "💼 Urgent Hiring: Financial Assistant. Handle transactions from home. ₹18k/week + bonus!",
    "📱 Instagram Opportunity: Be a payment coordinator. ₹25k/month. DM for details!",
    "🎯 Student-Friendly Job: Process payments part-time. ₹12k/week. No investment required!"
]

def show_victim_popup(account_id):
    """Show mock victim recruitment scenario"""
    fake_ad = random.choice(FAKE_JOB_ADS)
    
    st.markdown(f"""
    <div class="victim-popup">
        <h4>🎭 Likely Recruitment Scenario</h4>
        <p><strong>Account:</strong> {account_id}</p>
        <p><strong>Victim probably saw this ad:</strong></p>
        <p style="font-style: italic; padding: 10px; background: white; border-radius: 5px;">
            "{fake_ad}"
        </p>
        <p><strong>What happened next:</strong></p>
        <ul>
            <li>Victim responded thinking it's a legitimate job</li>
            <li>Scammer asked for bank details "for salary deposit"</li>
            <li>Account used to receive & transfer stolen money</li>
            <li>Victim unaware they're committing money laundering</li>
        </ul>
        <p style="color: #dc3545;"><strong>⚠️ 71% of Gen Z unaware this leads to criminal record</strong></p>
    </div>
    """, unsafe_allow_html=True)

def export_sar_report(flagged_accounts, rings):
    """Generate SAR (Suspicious Activity Report) export"""
    # Create comprehensive report
    report_data = []
    
    for acc in flagged_accounts[:50]:  # Top 50
        report_data.append({
            'Report_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Account_ID': acc['account_id'],
            'Risk_Score': acc['risk_score'],
            'Status': 'CRITICAL' if acc['risk_score'] >= 70 else 'HIGH',
            'Cyber_Flags': ', '.join(acc['cyber_flags']) if acc['cyber_flags'] else 'None',
            'Financial_Flags': ', '.join(acc['financial_flags']) if acc['financial_flags'] else 'None',
            'Recommended_Action': 'FREEZE_IMMEDIATELY' if acc['risk_score'] >= 80 else 'MANUAL_REVIEW',
            'Ring_Membership': 'Under Investigation'
        })
    
    report_df = pd.DataFrame(report_data)
    return report_df

# Main app
st.title("🛡️ CyberFin Fusion - Unified Cyber-Financial Intelligence")
st.markdown("**Stop the Money Before It Disappears**")

cyber_df, txn_df = load_data()
detector = initialize_detector(cyber_df, txn_df)
explainer = initialize_explainer()

# Sidebar
st.sidebar.header("⚙️ Controls")

# API Status indicator
if explainer.api_available:
    st.sidebar.success("✅ Gemini AI: Active", icon="🤖")
else:
    st.sidebar.warning("⚠️ Gemini AI: Fallback Mode", icon="⚠️")
    st.sidebar.info("Add GEMINI_API_KEY to .env for AI features. See GEMINI_API_SETUP.md")

risk_threshold = st.sidebar.slider("Risk Score Threshold", 0, 100, 50)

# Timeline filter
st.sidebar.subheader("📅 Timeline Filter")
min_time = cyber_df['timestamp'].min()
max_time = cyber_df['timestamp'].max()
time_range = st.sidebar.slider(
    "Select Time Range (hours ago)",
    min_value=0,
    max_value=24,
    value=(0, 24),
    help="Filter events by time range"
)

# Filter data by time
time_start = max_time - timedelta(hours=time_range[1])
time_end = max_time - timedelta(hours=time_range[0])
filtered_cyber = cyber_df[(cyber_df['timestamp'] >= time_start) & (cyber_df['timestamp'] <= time_end)]
filtered_txns = txn_df[(txn_df['timestamp'] >= time_start) & (txn_df['timestamp'] <= time_end)]

st.sidebar.info(f"📊 Showing {len(filtered_cyber):,} events and {len(filtered_txns):,} transactions")

view_mode = st.sidebar.radio("View Mode", ["Dashboard", "Live Graph", "Account Lookup", "Ring Analysis"])

# Export buttons in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Reports")

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
        st.metric("📊 Total Events", f"{len(filtered_cyber):,}")
    with col4:
        st.metric("💰 Total Transactions", f"{len(filtered_txns):,}")
    
    # Export SAR Report
    if st.sidebar.button("📄 Generate SAR Report", help="Export Suspicious Activity Report"):
        sar_report = export_sar_report(flagged_accounts, rings)
        csv = sar_report.to_csv(index=False)
        st.sidebar.download_button(
            label="⬇️ Download SAR Report",
            data=csv,
            file_name=f"SAR_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        st.sidebar.success("✅ SAR Report generated!")
    
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
    event_counts = filtered_cyber.groupby([pd.Grouper(key='timestamp', freq='1h'), 'event_type']).size().reset_index(name='count')
    
    fig_timeline = px.line(event_counts, x='timestamp', y='count', color='event_type',
                          title="Cyber Events Over Time")
    st.plotly_chart(fig_timeline, use_container_width=True)

elif view_mode == "Live Graph":
    st.subheader("🕸️ Network Graph Visualization")
    st.info("Showing connections between accounts, devices, IPs, and beneficiaries")
    st.warning("⚠️ Graph limited to 500 nodes for demo performance. Production systems handle millions of nodes.", icon="⚠️")
    
    # Select a ring to visualize
    rings = detector.detect_mule_rings()
    if rings:
        selected_ring = st.selectbox("Select Ring to Visualize", 
                                     [f"Ring {r['ring_id']} ({r['size']} accounts)" for r in rings[:10]])
        ring_idx = int(selected_ring.split()[1])
        
        ring = [r for r in rings if r['ring_id'] == ring_idx][0]
        
        # Create subgraph for this ring (limit to 500 nodes)
        subgraph = nx.Graph()
        node_count = 0
        MAX_NODES = 500
        
        for acc in ring['accounts']:
            if node_count >= MAX_NODES:
                st.warning(f"⚠️ Graph limited to {MAX_NODES} nodes. Ring has {len(ring['accounts'])} accounts total.")
                break
            neighbors = list(detector.graph.neighbors(acc))
            for neighbor in neighbors[:10]:  # Limit neighbors per account
                if node_count < MAX_NODES:
                    subgraph.add_edge(acc, neighbor)
                    node_count = len(subgraph.nodes())
        
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
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=f"Ring {ring_idx} Network ({len(subgraph.nodes())} nodes shown)",
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0,l=0,r=0,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write(f"**Accounts in Ring:** {', '.join(ring['accounts'][:10])}")
        st.write(f"**Shared Beneficiaries:** {', '.join(ring['shared_beneficiaries'])}")
        
        # Explain this ring button
        if st.button("🤖 Explain This Ring with AI"):
            with st.spinner("Generating AI explanation..."):
                ring_explanation = f"""
                Ring {ring_idx} contains {ring['size']} accounts all connected through shared beneficiaries.
                Shared beneficiaries: {', '.join(ring['shared_beneficiaries'][:3])}
                This pattern is highly suspicious for money mule activity.
                """
                
                # Use Gemini to explain
                account_data = {'account_id': f"Ring_{ring_idx}", 'risk_score': 85}
                explanation = explainer.explain_mule_pattern(
                    account_data,
                    ['multiple_accounts', 'shared_beneficiaries'],
                    ['rapid_transactions'],
                    {'size': ring['size'], 'beneficiaries': ring['shared_beneficiaries']}
                )
                
                st.markdown("### 🤖 AI Analysis")
                st.info(explanation)

elif view_mode == "Ring Analysis":
    st.subheader("🔍 Detailed Ring Analysis")
    
    rings = detector.detect_mule_rings()
    
    if rings:
        # Select ring
        ring_options = [f"Ring {r['ring_id']} - {r['size']} accounts" for r in rings[:20]]
        selected = st.selectbox("Select Ring for Analysis", ring_options)
        ring_idx = int(selected.split()[1])
        
        ring = [r for r in rings if r['ring_id'] == ring_idx][0]
        
        # Ring details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ring Size", f"{ring['size']} accounts")
        with col2:
            st.metric("Shared Beneficiaries", len(ring['shared_beneficiaries']))
        with col3:
            st.metric("Risk Level", "🔴 CRITICAL" if ring['size'] > 10 else "🟡 HIGH")
        
        # Show accounts
        st.subheader("📋 Accounts in Ring")
        st.write(", ".join(ring['accounts'][:20]))
        if len(ring['accounts']) > 20:
            st.info(f"... and {len(ring['accounts']) - 20} more accounts")
        
        # Show beneficiaries
        st.subheader("💰 Shared Beneficiaries")
        st.write(", ".join(ring['shared_beneficiaries']))
        
        # AI Explanation
        if st.button("🤖 Generate AI Explanation for This Ring"):
            with st.spinner("Analyzing ring pattern..."):
                account_data = {'account_id': f"Ring_{ring_idx}", 'risk_score': 85}
                explanation = explainer.explain_mule_pattern(
                    account_data,
                    ['multiple_accounts', 'shared_beneficiaries', 'coordinated_activity'],
                    ['rapid_transactions', 'near_threshold_amount'],
                    {'size': ring['size'], 'beneficiaries': ring['shared_beneficiaries']}
                )
                st.markdown("### 🤖 AI Analysis")
                st.info(explanation)
        
        # Show victim popup for random account
        if st.button("🎭 Show Likely Victim Scenario"):
            sample_account = random.choice(ring['accounts'][:10])
            show_victim_popup(sample_account)
        
        # Export ring data
        if st.button("📥 Export Ring Data"):
            ring_export = pd.DataFrame({
                'Ring_ID': [ring['ring_id']] * len(ring['accounts']),
                'Account_ID': ring['accounts'],
                'Shared_Beneficiaries': [', '.join(ring['shared_beneficiaries'])] * len(ring['accounts']),
                'Ring_Size': [ring['size']] * len(ring['accounts'])
            })
            csv = ring_export.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Ring Data",
                data=csv,
                file_name=f"Ring_{ring_idx}_Export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

elif view_mode == "Account Lookup":
    st.subheader("🔍 Account Risk Analysis")
    
    account_id = st.text_input("Enter Account ID (e.g., ACC_002747)")
    
    if account_id and st.button("Analyze"):
        if account_id in cyber_df['account_id'].values:
            risk_score = detector.calculate_risk_score(account_id)
            cyber_flags = detector.detect_cyber_anomalies(account_id)
            fin_flags = detector.detect_financial_velocity(account_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Risk Score", f"{risk_score}/100")
                
                if risk_score >= 70:
                    st.markdown('<div class="alert-critical">🚨 CRITICAL RISK</div>', unsafe_allow_html=True)
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
            
            # Victim scenario
            if risk_score >= 50:
                if st.button("🎭 Show Likely Recruitment Scenario"):
                    show_victim_popup(account_id)
            
            # Action buttons
            st.subheader("⚡ Quick Actions")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛑 Freeze Account"):
                    st.success("✅ Account frozen! All transactions blocked.")
            with col2:
                if st.button("📋 Generate SAR"):
                    sar_data = pd.DataFrame([{
                        'Account_ID': account_id,
                        'Risk_Score': risk_score,
                        'Cyber_Flags': ', '.join(cyber_flags),
                        'Financial_Flags': ', '.join(fin_flags),
                        'Report_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }])
                    csv = sar_data.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download SAR",
                        data=csv,
                        file_name=f"SAR_{account_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ SAR report generated!")
            with col3:
                if st.button("📞 Contact Customer"):
                    st.info("📧 Alert sent to account holder")
            
            # Additional AI-powered buttons
            st.subheader("🤖 AI-Powered Analysis")
            col4, col5 = st.columns(2)
            with col4:
                if st.button("📋 Generate SAR Narrative"):
                    with st.spinner("Generating professional SAR narrative..."):
                        sar_narrative = explainer.generate_sar_narrative(
                            {'account_id': account_id, 'risk_score': risk_score},
                            cyber_flags,
                            fin_flags
                        )
                        st.markdown(sar_narrative)
                
                if st.button("🔍 Investigation Steps"):
                    with st.spinner("Generating investigation plan..."):
                        all_flags = cyber_flags + fin_flags
                        steps = explainer.suggest_investigation_steps(
                            {'account_id': account_id, 'risk_score': risk_score},
                            all_flags
                        )
                        st.markdown(steps)
            
            with col5:
                if st.button("🛡️ Prevention Tips"):
                    with st.spinner("Generating prevention guidance..."):
                        tips = explainer.explain_prevention_tips("money_mule")
                        st.markdown(tips)
                
                if st.button("📖 Victim Education"):
                    with st.spinner("Generating victim scenario..."):
                        scenario = explainer.generate_victim_scenario(
                            {'account_id': account_id, 'risk_score': risk_score}
                        )
                        st.info(scenario)
        else:
            st.error("Account not found")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**CyberFin Fusion v2.0**")
st.sidebar.markdown("Enhanced with AI & Polish")
st.sidebar.markdown("Built for 24hr Hackathon")
