import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Load investment data
DATA_PATH = os.path.join(PROJECT_ROOT, "datasets", "investment_data.json")
try:
    with open(DATA_PATH, 'r') as f:
        INVESTMENT_DATA = json.load(f)
except:
    INVESTMENT_DATA = {}

# Import new modules - ENHANCED VERSIONS
try:
    from src.rag_tax_advisor_enhanced import EnhancedRAGTaxAdvisor
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Enhanced RAG Tax Advisor not available")

try:
    from src.itr_risk_shap_enhanced import EnhancedITRRiskAnalyzer
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("Enhanced SHAP Risk Analyzer not available")

try:
    from src.lstm_tax_predictor import LSTMTaxPredictor
    LSTM_AVAILABLE = True
except ImportError:
    LSTM_AVAILABLE = False
    print("LSTM Tax Predictor not available")

# Import Investment Optimizer modules
try:
    from src.investment_optimizer import (
        UserFinancialProfile, optimize_elss_investment,
        analyze_home_loan_vs_rent, create_monthly_investment_plan,
        LIMIT_80C, LIMIT_80D_SELF, LIMIT_80CCD_1B, LIMIT_24B
    )
    OPTIMIZER_AVAILABLE = True
except ImportError as e:
    OPTIMIZER_AVAILABLE = False
    # Only print error once during development
    import sys
    if 'OPTIMIZER_ERROR_LOGGED' not in sys.modules:
        sys.modules['OPTIMIZER_ERROR_LOGGED'] = True
        print(f"Investment Optimizer import error: {e}")

# ======================================================
# PAGE CONFIG & STYLING
# ======================================================
st.set_page_config(page_title="Tax Saver AI", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    :root {
        --primary: #6366f1; --secondary: #10b981; --warning: #f59e0b; --danger: #ef4444;
        --background: #0f172a; --surface: #1e293b; --surface-light: #334155;
        --text-primary: #f8fafc; --text-secondary: #94a3b8; --border: #334155;
    }
    .stApp { background: var(--background); font-family: 'Plus Jakarta Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-right: 1px solid var(--border); }
    .main-header { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 2rem 2.5rem; border-radius: 20px; margin-bottom: 2rem; }
    .main-header h1 { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; }
    .main-header p { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 0.5rem; }
    .section-header { display: flex; align-items: center; gap: 12px; margin: 1.5rem 0 1rem 0; padding-bottom: 0.75rem; border-bottom: 2px solid var(--border); }
    .section-header h3 { color: var(--text-primary); font-size: 1.25rem; font-weight: 600; margin: 0; }
    .section-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    .metric-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; text-align: center; transition: all 0.3s ease; }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
    .metric-value { font-size: 2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .metric-label { color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; }
    .strategy-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 0.5rem 0; }
    .strategy-card.recommended { border: 2px solid var(--secondary); background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, var(--surface) 100%); }
    .timeline-item { display: flex; gap: 1rem; padding: 1rem 0; border-left: 2px solid var(--border); padding-left: 1.5rem; margin-left: 0.5rem; position: relative; }
    .timeline-item::before { content: ''; position: absolute; left: -6px; top: 1.25rem; width: 10px; height: 10px; border-radius: 50%; background: var(--primary); }
    .divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 2rem 0; }
    .chat-message { padding: 1rem; border-radius: 12px; margin: 0.5rem 0; }
    .chat-message.user { background: rgba(99, 102, 241, 0.1); border-left: 3px solid #6366f1; }
    .chat-message.assistant { background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; }
    .source-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
    .footer { text-align: center; padding: 2rem; color: var(--text-secondary); font-size: 0.9rem; margin-top: 3rem; border-top: 1px solid var(--border); }
    .stButton > button { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.75rem 2rem !important; font-weight: 600 !important; width: 100%; }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: var(--surface); padding: 8px; border-radius: 14px; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 10px !important; color: var(--text-secondary) !important; padding: 10px 20px !important; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def format_currency(amount):
    if amount >= 10000000: return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000: return f"₹{amount/100000:.2f} L"
    else: return f"₹{amount:,.0f}"

def format_inr(amount): return f"₹{amount:,.0f}"

def compute_tax(taxable_income):
    """Calculate tax under New Tax Regime (Mandatory from FY 2025-26)"""
    tax = 0.0
    slabs = [(0, 300000, 0.0), (300000, 600000, 0.05), (600000, 900000, 0.10), (900000, 1200000, 0.15), (1200000, 1500000, 0.20), (1500000, float("inf"), 0.30)]
    for lower, upper, rate in slabs:
        if taxable_income > lower: tax += (min(taxable_income, upper) - lower) * rate
    return 0.0 if taxable_income <= 700000 else tax * 1.04

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">Tax Saver AI</div>
        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem;">Smart Tax Assistant v2.0</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        [
            "🤖 RAG Tax Advisor",
            "📈 Investment Optimizer",
            "🚨 ITR Risk Check",
            "📊 Tax Prediction (LSTM)"
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 1rem; background: rgba(99, 102, 241, 0.1); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
        <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.5rem;">💡 Quick Tip</div>
        <div style="font-size: 0.85rem; color: #f8fafc; line-height: 1.5;">Ask the RAG Tax Advisor any tax-related questions and get AI-powered answers!</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# 1️⃣ RAG TAX ADVISOR
# ======================================================
if page == "🤖 RAG Tax Advisor":
    st.markdown('<div class="main-header"><h1>🤖 RAG Tax Advisor</h1><p>AI-powered tax advisor using Retrieval-Augmented Generation with Gemini</p></div>', unsafe_allow_html=True)

    if not RAG_AVAILABLE:
        st.error("⚠️ RAG Tax Advisor module not available. Please ensure rag_tax_advisor.py is in the src folder.")
    else:
        # Initialize Enhanced RAG advisor
        if 'rag_advisor' not in st.session_state:
            gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCG7VZO0f88v-4tfkR5EZnXG68-_an_0Ho')
            st.session_state.rag_advisor = EnhancedRAGTaxAdvisor(api_key=gemini_api_key)

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        if 'current_response' not in st.session_state:
            st.session_state.current_response = None

        # Input area - MOVED TO TOP
        st.markdown('<div class="section-header"><div class="section-icon">❓</div><h3>Ask a Question</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            user_query = st.text_input("Enter your tax question", placeholder="e.g., What is Section 80C?", key="tax_query")
        with col2:
            ask_button = st.button("Ask", use_container_width=True)

        # Quick questions
        st.markdown("**Quick Questions:**")
        quick_questions = [
            "What is Section 80C?",
            "How to claim HRA exemption?",
            "What is the ITR filing deadline?",
            "Difference between old and new tax regime?"
        ]

        cols = st.columns(2)
        for i, q in enumerate(quick_questions):
            with cols[i % 2]:
                if st.button(q, key=f"quick_{i}"):
                    user_query = q
                    ask_button = True

        # Process query
        if ask_button and user_query:
            with st.spinner("Thinking..."):
                result = st.session_state.rag_advisor.ask(user_query)

                # Store current response
                st.session_state.current_response = result

                # Add to chat history
                st.session_state.chat_history.append(result)

        # Display current response IMMEDIATELY BELOW question
        if st.session_state.current_response:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="section-icon">💡</div><h3>Response</h3></div>', unsafe_allow_html=True)

            response = st.session_state.current_response

            # Display question
            st.markdown(f'''<div class="chat-message user">
                <strong>You:</strong> {response['query']}
            </div>''', unsafe_allow_html=True)

            # Display answer - Separate markdown to avoid HTML breaking
            st.markdown('<div class="chat-message assistant">', unsafe_allow_html=True)
            st.markdown("**Assistant:**")
            st.markdown(response['answer'])
            st.markdown('</div>', unsafe_allow_html=True)

            # Display metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**LLM Used:** {'Yes' if response.get('llm_used') else 'No'}")
            with col2:
                st.markdown(f"**Calculation:** {'Yes' if response.get('calculation_performed') else 'No'}")
            with col3:
                st.markdown(f"**Sources:** {len(response.get('sources', []))} documents")

            # Display sources
            if response.get('sources'):
                with st.expander(f"📚 View Sources ({len(response['sources'])} documents)", expanded=False):
                    for j, source in enumerate(response['sources'][:3], 1):
                        st.markdown(f'''<div class="source-card">
                            <div style="font-weight: 600; color: #10b981;">Source {j}: {source['question']}</div>
                            <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">{source['answer'][:200]}...</div>
                            <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">
                                Category: {source['category']} | Relevance: {source['relevance_score']:.2f}
                            </div>
                        </div>''', unsafe_allow_html=True)

        # Chat History section (below current response)
        if st.session_state.chat_history:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="section-icon">💬</div><h3>Chat History</h3></div>', unsafe_allow_html=True)

            # Show only past conversations (not the current one)
            history_to_show = st.session_state.chat_history[:-1] if st.session_state.current_response else st.session_state.chat_history

            for i, chat in enumerate(reversed(history_to_show)):  # Show newest first
                with st.expander(f"Q: {chat['query'][:100]}..." if len(chat['query']) > 100 else f"Q: {chat['query']}", expanded=False):
                    st.markdown(chat['answer'])

        # Browse categories
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-icon">📑</div><h3>Browse by Category</h3></div>', unsafe_allow_html=True)

        categories = st.session_state.rag_advisor.get_categories()
        selected_category = st.selectbox("Select Category", categories)

        if selected_category:
            category_docs = st.session_state.rag_advisor.search_by_category(selected_category)
            st.markdown(f"**{len(category_docs)} FAQs in {selected_category}:**")

            for doc in category_docs:
                with st.expander(f"❓ {doc['question']}", expanded=False):
                    st.markdown(f"**Answer:** {doc['answer']}")
                    st.markdown(f"**Keywords:** {', '.join(doc['keywords'])}")

# ======================================================
# 2️⃣ INVESTMENT OPTIMIZER
# ======================================================
elif page == "📈 Investment Optimizer":
    st.markdown('<div class="main-header" style="background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);"><h1>📈 Investment Optimizer</h1><p>Smart investment planning and wealth management tools</p></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 ELSS Optimizer", "🏠 Buy vs Rent", "📅 Monthly Planner", "🎯 What-If Simulator"])

    # TAB 1: ELSS OPTIMIZER
    with tab1:
        st.markdown('<div class="section-header"><div class="section-icon">📊</div><h3>ELSS SIP vs Lump Sum Optimizer</h3></div>', unsafe_allow_html=True)

        # Market Timing Indicator
        if INVESTMENT_DATA.get('market_timing_indicators'):
            mti = INVESTMENT_DATA['market_timing_indicators']
            nifty_pe = mti.get('nifty_pe', {})
            current_pe = nifty_pe.get('current', 22.5)
            avg_pe = nifty_pe.get('5yr_avg', 24.2)
            market_status = mti.get('sip_vs_lumpsum_analysis', {}).get('current_market', 'Moderately Valued')

            pe_color = '#10b981' if current_pe < 20 else '#f59e0b' if current_pe < 26 else '#ef4444'
            st.markdown(f'''<div style="background: linear-gradient(135deg, var(--surface) 0%, rgba(99, 102, 241, 0.1) 100%);
                border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div><div style="color: #94a3b8; font-size: 0.85rem;">📈 Nifty PE Ratio</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: {pe_color};">{current_pe}</div>
                        <div style="color: #64748b; font-size: 0.75rem;">5Y Avg: {avg_pe}</div></div>
                    <div><div style="color: #94a3b8; font-size: 0.85rem;">🎯 Market Status</div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc;">{market_status}</div></div>
                    <div><div style="color: #94a3b8; font-size: 0.85rem;">💡 Current Recommendation</div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: #10b981;">{"SIP" if current_pe > 22 else "Lump Sum"}</div></div>
                </div>
            </div>''', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            elss_amount = st.number_input("ELSS Investment (₹)", min_value=10000, max_value=150000, value=50000, step=10000, key="elss_amt")
            expected_return = st.slider("Expected Return (%)", min_value=8, max_value=25, value=12, key="elss_ret")
        with col2:
            risk_tolerance = st.select_slider("Risk Tolerance", options=["Conservative", "Moderate", "Aggressive"], value="Moderate")
            holding_years = st.number_input("Holding Years", min_value=3, max_value=10, value=5, key="elss_hold")

        if st.button("🎯 Optimize ELSS Strategy", use_container_width=True, key="elss_btn"):
            monthly_sip = elss_amount / 12
            monthly_return = (1 + expected_return/100) ** (1/12) - 1

            # SIP future value
            sip_fv = sum([monthly_sip * ((1 + monthly_return) ** (holding_years * 12 - m)) for m in range(holding_years * 12)])
            lump_fv = elss_amount * ((1 + expected_return/100) ** holding_years)

            is_sip = risk_tolerance == "Conservative" or (INVESTMENT_DATA.get('market_timing_indicators', {}).get('nifty_pe', {}).get('current', 22) > 23)
            tax_benefit = elss_amount * 0.312

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown(f'''<div style="background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><div style="color: #94a3b8; font-size: 0.9rem;">Investment</div><div style="color: #f8fafc; font-size: 1.5rem; font-weight: 600;">{format_inr(elss_amount)}</div></div>
                    <div style="font-size: 2rem;">→</div>
                    <div style="text-align: right;"><div style="color: #94a3b8; font-size: 0.9rem;">Tax Benefit (31.2%)</div><div style="color: #10b981; font-size: 1.5rem; font-weight: 600;">{format_inr(tax_benefit)}</div></div>
                </div>
            </div>''', unsafe_allow_html=True)

            s1, s2 = st.columns(2)
            with s1:
                rec = "⭐ RECOMMENDED" if is_sip else ""
                card_class = "recommended" if is_sip else ""
                sip_gain = sip_fv - elss_amount
                st.markdown(f'''<div class="strategy-card {card_class}">
                    <h4 style="color: #6366f1; margin-bottom: 1rem;">📅 SIP Strategy {rec}</h4>
                    <div style="font-size: 1.25rem; font-weight: 600; color: #f8fafc;">{format_inr(monthly_sip)}/month</div>
                    <div style="color: #94a3b8; font-size: 0.9rem; margin: 0.5rem 0;">Expected Value ({holding_years}Y): <span style="color: #10b981; font-weight: 600;">{format_currency(sip_fv)}</span></div>
                    <div style="color: #f8fafc; font-size: 0.9rem;">Expected Gain: <span style="color: #10b981;">{format_currency(sip_gain)}</span></div>
                    <div style="color: #10b981; font-size: 0.85rem; margin-top: 1rem;">✅ Rupee cost averaging, Lower risk</div>
                    <div style="color: #ef4444; font-size: 0.85rem;">❌ Slightly lower returns</div>
                </div>''', unsafe_allow_html=True)

            with s2:
                rec = "⭐ RECOMMENDED" if not is_sip else ""
                card_class = "recommended" if not is_sip else ""
                lump_gain = lump_fv - elss_amount
                st.markdown(f'''<div class="strategy-card {card_class}">
                    <h4 style="color: #f59e0b; margin-bottom: 1rem;">💰 Lump Sum {rec}</h4>
                    <div style="font-size: 1.25rem; font-weight: 600; color: #f8fafc;">{format_inr(elss_amount)} in April</div>
                    <div style="color: #94a3b8; font-size: 0.9rem; margin: 0.5rem 0;">Expected Value ({holding_years}Y): <span style="color: #10b981; font-weight: 600;">{format_currency(lump_fv)}</span></div>
                    <div style="color: #f8fafc; font-size: 0.9rem;">Expected Gain: <span style="color: #10b981;">{format_currency(lump_gain)}</span></div>
                    <div style="color: #10b981; font-size: 0.85rem; margin-top: 1rem;">✅ Max time in market, Higher returns</div>
                    <div style="color: #ef4444; font-size: 0.85rem;">❌ Timing risk</div>
                </div>''', unsafe_allow_html=True)

            # Investment Calendar Chart
            months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
            if is_sip:
                investments = [monthly_sip] * 12
                cumulative = [monthly_sip * (i+1) for i in range(12)]
            else:
                investments = [elss_amount] + [0] * 11
                cumulative = [elss_amount] * 12

            fig = go.Figure()
            fig.add_trace(go.Bar(x=months, y=investments, name="Investment", marker_color='#6366f1'))
            fig.add_trace(go.Scatter(x=months, y=cumulative, name="Cumulative", line=dict(color='#10b981', width=3), mode='lines+markers'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'),
                              legend=dict(orientation='h', yanchor='bottom', y=1.02), height=300, margin=dict(l=20, r=20, t=40, b=20),
                              yaxis=dict(gridcolor='rgba(51, 65, 85, 0.5)', title='Amount (₹)'))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # TAB 2: BUY VS RENT
    with tab2:
        st.markdown('<div class="section-header"><div class="section-icon">🏠</div><h3>Home Loan vs Rent Analyzer</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            property_value = st.number_input("Property Value (₹)", min_value=1000000, value=5000000, step=500000, key="prop_val")
            loan_amount = st.number_input("Loan Amount (₹)", min_value=500000, value=4000000, step=500000, key="loan_amt")
            loan_tenure = st.number_input("Tenure (Years)", min_value=5, max_value=30, value=20, key="loan_ten")

        with col2:
            interest_rate = st.number_input("Interest Rate (%)", min_value=6.0, max_value=12.0, value=8.5, step=0.1, key="int_rate")
            monthly_rent = st.number_input("Current Rent (₹/month)", min_value=5000, value=25000, step=5000, key="rent_m")
            rent_increase = st.number_input("Rent Increase (%/year)", min_value=0.0, max_value=15.0, value=5.0, step=0.5, key="rent_inc")

        if st.button("🏠 Analyze Buy vs Rent", use_container_width=True, key="home_btn"):
            # EMI Calculation
            monthly_rate = (interest_rate / 100) / 12
            num_payments = loan_tenure * 12
            emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** num_payments) / (((1 + monthly_rate) ** num_payments) - 1)

            total_payment = emi * num_payments
            total_interest = total_payment - loan_amount
            down_payment = property_value - loan_amount

            # Simplified tax benefit calculation
            avg_annual_interest = total_interest / loan_tenure
            tax_benefit_per_year = min(avg_annual_interest, 200000) * 0.312
            total_tax_benefit = tax_benefit_per_year * loan_tenure

            # Property value projection
            prop_appreciation = 6.0
            final_value = property_value * ((1 + prop_appreciation / 100) ** loan_tenure)

            # Rent projection
            total_rent = 0
            current_monthly_rent = monthly_rent
            for year in range(loan_tenure):
                total_rent += current_monthly_rent * 12
                current_monthly_rent *= (1 + rent_increase/100)

            # Net positions
            home_net = final_value - total_payment - down_payment + total_tax_benefit
            rent_net = (down_payment * ((1.10) ** loan_tenure)) - total_rent

            recommendation = "BUY" if home_net > rent_net else "RENT"

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(f'<div class="metric-card"><div class="metric-value">{format_inr(emi)}</div><div class="metric-label">Monthly EMI</div></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="metric-card"><div class="metric-value">{format_currency(total_interest)}</div><div class="metric-label">Total Interest</div></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="metric-card"><div class="metric-value" style="background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text;">{format_currency(total_tax_benefit)}</div><div class="metric-label">Tax Benefits</div></div>', unsafe_allow_html=True)
            with m4: st.markdown(f'<div class="metric-card"><div class="metric-value">{format_currency(final_value)}</div><div class="metric-label">Property Value ({loan_tenure}Y)</div></div>', unsafe_allow_html=True)

            rec_color = "#10b981" if recommendation == "BUY" else "#f59e0b"
            st.markdown(f'''<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
                border: 2px solid {rec_color}; border-radius: 20px; padding: 2rem; margin-top: 1.5rem; text-align: center;">
                <div style="font-size: 3rem;">{"🏠" if recommendation == "BUY" else "🏢"}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {rec_color};">Recommendation: {recommendation}</div>
                <div style="color: #94a3b8; font-size: 1.1rem;">{"Buying" if recommendation == "BUY" else "Renting"} builds {format_inr(abs(home_net - rent_net))} more wealth</div>
            </div>''', unsafe_allow_html=True)

    # TAB 3: MONTHLY PLANNER
    with tab3:
        st.markdown('<div class="section-header"><div class="section-icon">📅</div><h3>Monthly Investment Planner</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            current_80c = st.number_input("Current 80C (₹)", min_value=0, max_value=150000, value=0, step=10000, key="plan_80c")
            current_nps = st.number_input("Current NPS (₹)", min_value=0, max_value=50000, value=0, step=5000, key="plan_nps")
            current_80d = st.number_input("Current 80D (₹)", min_value=0, max_value=50000, value=0, step=5000, key="plan_80d")
        with col2:
            start_month = st.selectbox("Start Planning From", ["April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"], key="start_m")

        if st.button("📅 Generate Investment Plan", use_container_width=True, key="plan_btn"):
            # Create investment plan using the optimizer function
            current_investments = {
                '80c': current_80c,
                'nps': current_nps,
                'health_insurance': current_80d
            }

            plan_result = create_monthly_investment_plan(
                annual_salary=1000000,  # Dummy value, not used in calculation
                current_investments=current_investments
            )

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # Summary metrics
            g1, g2, g3, g4 = st.columns(4)
            with g1: st.markdown(f'<div class="metric-card"><div class="metric-value">{format_inr(plan_result["total_investment_needed"])}</div><div class="metric-label">To Invest</div></div>', unsafe_allow_html=True)
            with g2: st.markdown(f'<div class="metric-card"><div class="metric-value">{format_inr(plan_result["monthly_target"])}</div><div class="metric-label">Monthly</div></div>', unsafe_allow_html=True)
            with g3: st.markdown(f'<div class="metric-card"><div class="metric-value" style="background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text;">{format_inr(plan_result["total_tax_savings"])}</div><div class="metric-label">Tax Saved</div></div>', unsafe_allow_html=True)
            with g4: st.markdown(f'<div class="metric-card"><div class="metric-value">12</div><div class="metric-label">Months Left</div></div>', unsafe_allow_html=True)

            # MONTHLY INVESTMENT PLAN TABLE
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="section-icon">📊</div><h3>Month-by-Month Investment Plan</h3></div>', unsafe_allow_html=True)

            # Explanation of components
            st.markdown("""
                <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                    <div style="color: #c7d2fe; font-weight: 600; margin-bottom: 1rem;">📖 Understanding Your Investment Plan</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.8;">
                        <div style="margin-bottom: 0.8rem;">
                            <strong style="color: #a5b4fc;">💰 ELSS SIP (80C):</strong>
                            Equity Linked Savings Scheme - Invest monthly in tax-saving mutual funds.
                            <span style="color: #94a3b8;">Spreads your investment throughout the year for rupee cost averaging.</span>
                        </div>
                        <div style="margin-bottom: 0.8rem;">
                            <strong style="color: #a5b4fc;">🏦 NPS (80CCD):</strong>
                            National Pension System - Retirement savings with additional tax benefits.
                            <span style="color: #94a3b8;">Contributed quarterly for long-term wealth building.</span>
                        </div>
                        <div style="margin-bottom: 0.8rem;">
                            <strong style="color: #a5b4fc;">🏥 Health Insurance (80D):</strong>
                            Medical insurance premium - Paid annually in April.
                            <span style="color: #94a3b8;">Protects you from medical emergencies while building wealth.</span>
                        </div>
                        <div style="margin-bottom: 0.8rem;">
                            <strong style="color: #a5b4fc;">📊 Monthly Total:</strong>
                            Total amount to invest in that specific month.
                        </div>
                        <div>
                            <strong style="color: #a5b4fc;">💵 Cumulative Tax Saved:</strong>
                            Total tax savings accumulated up to that month (at 31.2% tax rate).
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Create detailed table
            table_data = []
            for month_plan in plan_result["plan"]:
                month_name = month_plan["month"]

                # Extract investment details
                elss_amount = 0
                nps_amount = 0
                insurance_amount = 0

                for inv in month_plan["investments"]:
                    if inv["type"] == "ELSS SIP":
                        elss_amount = inv["amount"]
                    elif inv["type"] == "NPS Contribution":
                        nps_amount = inv["amount"]
                    elif inv["type"] == "Health Insurance Premium":
                        insurance_amount = inv["amount"]

                table_data.append({
                    "Month": month_name,
                    "ELSS SIP (80C)": f"₹{elss_amount:,.0f}" if elss_amount > 0 else "-",
                    "NPS (80CCD)": f"₹{nps_amount:,.0f}" if nps_amount > 0 else "-",
                    "Health Insurance (80D)": f"₹{insurance_amount:,.0f}" if insurance_amount > 0 else "-",
                    "Monthly Total": f"₹{month_plan['total']:,.0f}",
                    "Cumulative Tax Saved": f"₹{month_plan['cumulative_tax_saved']:,.0f}"
                })

            # Add total row
            total_elss = sum(inv["amount"] for month in plan_result["plan"] for inv in month["investments"] if inv["type"] == "ELSS SIP")
            total_nps = sum(inv["amount"] for month in plan_result["plan"] for inv in month["investments"] if inv["type"] == "NPS Contribution")
            total_insurance = sum(inv["amount"] for month in plan_result["plan"] for inv in month["investments"] if inv["type"] == "Health Insurance Premium")

            table_data.append({
                "Month": "**TOTAL**",
                "ELSS SIP (80C)": f"**₹{total_elss:,.0f}**",
                "NPS (80CCD)": f"**₹{total_nps:,.0f}**",
                "Health Insurance (80D)": f"**₹{total_insurance:,.0f}**",
                "Monthly Total": f"**₹{plan_result['total_investment_needed']:,.0f}**",
                "Cumulative Tax Saved": f"**₹{plan_result['total_tax_savings']:,.0f}**"
            })

            # Display as clean Streamlit dataframe
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Action Items
            st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-radius: 12px; padding: 1.5rem; margin-top: 1.5rem;">
                    <div style="color: #6ee7b7; font-weight: 600; margin-bottom: 1rem;">✅ What to Do Next</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.8;">
                        <div style="margin-bottom: 0.5rem;">1️⃣ <strong>Set up monthly SIP</strong> for ELSS mutual funds - Auto-debit from your bank account</div>
                        <div style="margin-bottom: 0.5rem;">2️⃣ <strong>Open NPS account</strong> if you don't have one - Visit eNPS website or your bank</div>
                        <div style="margin-bottom: 0.5rem;">3️⃣ <strong>Pay health insurance premium</strong> in April - Get policy documents for tax filing</div>
                        <div style="margin-bottom: 0.5rem;">4️⃣ <strong>Set reminders</strong> for NPS contributions (April, July, October, January)</div>
                        <div>5️⃣ <strong>Keep investment proofs</strong> - Required for ITR filing by July 31</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Important Note
            st.markdown("""
                <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 1rem; margin-top: 1.5rem; border-radius: 8px;">
                    <div style="color: #fca5a5; font-weight: 600; margin-bottom: 0.5rem;">⚠️ Important Note - New Tax Regime (FY 2025-26)</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">
                        Under the New Tax Regime (mandatory from FY 2025-26), investments in 80C, 80D, and NPS do <strong>NOT provide tax deductions</strong>.
                        This plan is for <strong>wealth creation only</strong>, not tax savings under the new regime.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # TAB 4: WHAT-IF SIMULATOR
    with tab4:
        st.markdown('<div class="section-header"><div class="section-icon">🎯</div><h3>What-If Tax Scenario Simulator</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("**📊 Base Scenario**", unsafe_allow_html=True)
            base_salary = st.number_input("Annual Salary (₹)", min_value=0, value=800000, step=50000, key="sim_sal")
            base_other_income = st.number_input("Other Income (₹)", min_value=0, value=0, step=10000, key="sim_other")

        with col2:
            st.markdown("**🔄 Modified Scenario**", unsafe_allow_html=True)
            mod_salary = st.number_input("Annual Salary (₹)", min_value=0, value=1000000, step=50000, key="sim_sal2")
            mod_other_income = st.number_input("Other Income (₹)", min_value=0, value=0, step=10000, key="sim_other2")

        # Calculate taxes
        base_gross = base_salary + base_other_income
        mod_gross = mod_salary + mod_other_income

        base_taxable = max(0, base_gross - 50000)
        mod_taxable = max(0, mod_gross - 50000)

        base_tax = compute_tax(base_taxable)
        mod_tax = compute_tax(mod_taxable)

        tax_diff = base_tax - mod_tax
        income_diff = mod_gross - base_gross

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f'''<div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.85rem;">Base Tax</div>
                <div class="metric-value">{format_inr(base_tax)}</div>
            </div>''', unsafe_allow_html=True)
        with r2:
            st.markdown(f'''<div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.85rem;">Modified Tax</div>
                <div class="metric-value">{format_inr(mod_tax)}</div>
            </div>''', unsafe_allow_html=True)
        with r3:
            diff_color = '#10b981' if tax_diff > 0 else '#ef4444'
            diff_icon = '📉' if tax_diff > 0 else '📈'
            st.markdown(f'''<div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.85rem;">Tax Impact</div>
                <div class="metric-value" style="background: linear-gradient(135deg, {diff_color} 0%, #06b6d4 100%); -webkit-background-clip: text;">
                    {diff_icon} {format_inr(abs(tax_diff))}
                </div>
                <div style="color: {diff_color}; font-size: 0.85rem;">{"Savings" if tax_diff > 0 else "Increase"}</div>
            </div>''', unsafe_allow_html=True)

# ======================================================
# 3️⃣ ITR RISK CHECK WITH SHAP
# ======================================================
elif page == "🚨 ITR Risk Check":
    st.markdown('<div class="main-header" style="background: linear-gradient(135deg, #ef4444 0%, #f59e0b 100%);"><h1>🚨 Enhanced ITR Risk Check</h1><p>AI-powered risk prediction with SHAP explainability</p></div>', unsafe_allow_html=True)

    if not SHAP_AVAILABLE:
        st.error("⚠️ SHAP Risk Analyzer module not available. Please ensure itr_risk_shap.py is in the src folder.")
    else:
        # Initialize Enhanced analyzer
        if 'risk_analyzer' not in st.session_state:
            st.session_state.risk_analyzer = EnhancedITRRiskAnalyzer()

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            name = st.text_input("Full Name", key="risk_name")
            annual_salary = st.number_input("Annual Salary (₹)", min_value=0, step=50000, key="risk_sal")
            rent_paid = st.number_input("Rent Paid (₹/year)", min_value=0, step=10000, key="risk_rent")

        with col2:
            inv_80c = st.number_input("80C Investments (₹)", min_value=0, step=10000, key="risk_80c")
            med_80d = st.number_input("80D Health Insurance (₹)", min_value=0, step=5000, key="risk_80d")
            home_loan = st.number_input("Home Loan Interest 24(b) (₹)", min_value=0, step=10000, key="risk_loan")
            donations = st.number_input("Donations 80G (₹)", min_value=0, step=5000, key="risk_don")

        if st.button("🔍 Analyze Risk with SHAP", use_container_width=True, key="risk_btn"):
            # Prepare data
            user_data = {
                "Annual_Salary": annual_salary,
                "Investment_80C": inv_80c,
                "Medical_Insurance_80D": med_80d,
                "Home_Loan_Interest_24b": home_loan,
                "Donations_80G": donations,
                "Rent_Paid": rent_paid
            }

            with st.spinner("Analyzing with AI and generating SHAP explanations..."):
                result = st.session_state.risk_analyzer.analyze(user_data)

            score = result['risk_score']
            color = result['risk_color']
            level = result['risk_level']

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f'''<div style="text-align: center; padding: 2rem;">
                <div style="font-size: 5rem; font-weight: 700; color: {color}; font-family: JetBrains Mono;">{score}</div>
                <div style="font-size: 1.25rem; color: #94a3b8;">Risk Score (out of 100)</div>
                <div style="font-size: 1.5rem; font-weight: 600; color: {color}; margin-top: 0.5rem;">Risk Level: {level}</div>
            </div>''', unsafe_allow_html=True)

            # SHAP Explanations
            if result['success'] and result.get('shap_explanations'):
                st.markdown('<div class="section-header"><div class="section-icon">🔍</div><h3>SHAP Explanations - Why This Score?</h3></div>', unsafe_allow_html=True)
                st.markdown("**Top 5 factors affecting your risk score:**")

                for i, exp in enumerate(result['shap_explanations'][:5], 1):
                    impact_color = "#ef4444" if exp['impact'] == "INCREASES" else "#10b981"
                    st.markdown(f'''<div style="background: var(--surface); border-left: 4px solid {impact_color}; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;">
                        <div style="font-weight: 600; color: #f8fafc; margin-bottom: 0.5rem;">{i}. {exp['feature']}</div>
                        <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.25rem;">Value: ₹{exp['value']:,.0f}</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.25rem; color: {impact_color};">{exp['direction']}</span>
                            <span style="color: {impact_color}; font-size: 0.85rem; font-weight: 600;">{exp['impact']} risk by {exp['importance_percentage']:.1f}%</span>
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; padding: 0.5rem; background: rgba(0,0,0,0.2); border-radius: 8px;">
                            💡 {exp['explanation']}
                        </div>
                    </div>''', unsafe_allow_html=True)

                # Visualization
                st.markdown('<div class="section-header"><div class="section-icon">📊</div><h3>Feature Impact Visualization</h3></div>', unsafe_allow_html=True)

                features = [exp['feature'] for exp in result['shap_explanations'][:5]]
                shap_values = [exp['shap_value'] for exp in result['shap_explanations'][:5]]
                colors = ['#ef4444' if val > 0 else '#10b981' for val in shap_values]

                fig = go.Figure(go.Bar(
                    x=shap_values,
                    y=features,
                    orientation='h',
                    marker_color=colors
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(title='SHAP Value (Impact on Risk)', gridcolor='rgba(51, 65, 85, 0.5)'),
                    yaxis=dict(gridcolor='rgba(51, 65, 85, 0.5)')
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                # Overall Interpretation
                if result.get('overall_interpretation'):
                    st.markdown('<div class="section-header"><div class="section-icon">📋</div><h3>Overall Risk Assessment</h3></div>', unsafe_allow_html=True)
                    st.markdown('<div style="background: var(--surface); border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">', unsafe_allow_html=True)
                    st.markdown(result['overall_interpretation'])
                    st.markdown('</div>', unsafe_allow_html=True)

            # Risk Flags
            st.markdown('<div class="section-header"><div class="section-icon">⚠️</div><h3>Risk Flags</h3></div>', unsafe_allow_html=True)
            for flag in result['flags']:
                is_ok = "normal" in flag.lower() or "low" in level.lower()
                icon, bg, border = ("✅", "rgba(16, 185, 129, 0.1)", "rgba(16, 185, 129, 0.3)") if is_ok else ("⚠️", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)")
                st.markdown(f'<div style="background: {bg}; border: 1px solid {border}; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; display: flex; align-items: center; gap: 12px;"><span style="font-size: 1.25rem;">{icon}</span><span style="color: #f8fafc;">{flag}</span></div>', unsafe_allow_html=True)

# ======================================================
# 4️⃣ LSTM TAX PREDICTION
# ======================================================
elif page == "📊 Tax Prediction (LSTM)":
    st.markdown('<div class="main-header" style="background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);"><h1>📊 Tax Liability Prediction</h1><p>LSTM-powered future tax liability forecasting</p></div>', unsafe_allow_html=True)

    if not LSTM_AVAILABLE:
        st.error("⚠️ LSTM Tax Predictor module not available. Please ensure lstm_tax_predictor.py is in the src folder.")
    else:
        # Initialize predictor
        if 'lstm_predictor' not in st.session_state:
            st.session_state.lstm_predictor = LSTMTaxPredictor()

        st.markdown('<div class="section-header"><div class="section-icon">📈</div><h3>Historical Income Data</h3></div>', unsafe_allow_html=True)
        st.info("Enter your historical income data to predict future tax liability. Minimum 3 years recommended.")

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            year1 = st.number_input("Income 3 years ago (₹)", min_value=0, value=800000, step=50000, key="hist1")
            year2 = st.number_input("Income 2 years ago (₹)", min_value=0, value=850000, step=50000, key="hist2")
            year3 = st.number_input("Income last year (₹)", min_value=0, value=920000, step=50000, key="hist3")

        with col2:
            year4 = st.number_input("Current year income (₹)", min_value=0, value=1000000, step=50000, key="hist4")
            years_ahead = st.number_input("Predict for how many years?", min_value=1, max_value=10, value=3, key="years_pred")
            growth_rate = st.slider("Expected salary growth (%)", min_value=0, max_value=20, value=8, key="growth")

        if st.button("🔮 Predict Future Tax Liability", use_container_width=True, key="lstm_btn"):
            historical_incomes = [year1, year2, year3, year4]

            with st.spinner("Training LSTM model and predicting..."):
                # Train model
                st.session_state.lstm_predictor.train_model(historical_incomes, retrain=True)

                # Predict
                prediction = st.session_state.lstm_predictor.predict_future_tax(
                    historical_incomes,
                    years_ahead=years_ahead,
                    growth_rate=growth_rate/100
                )

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # Summary metrics
            total_future_tax = sum(prediction['future_taxes'])
            avg_effective_rate = sum(prediction['effective_rates']) / len(prediction['effective_rates'])

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value">{format_currency(total_future_tax)}</div>
                    <div class="metric-label">Total Tax ({years_ahead}Y)</div>
                </div>''', unsafe_allow_html=True)
            with m2:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value">{format_currency(total_future_tax/years_ahead)}</div>
                    <div class="metric-label">Avg Annual Tax</div>
                </div>''', unsafe_allow_html=True)
            with m3:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value" style="color: #f59e0b;">{avg_effective_rate:.1f}%</div>
                    <div class="metric-label">Avg Tax Rate</div>
                </div>''', unsafe_allow_html=True)
            with m4:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value" style="color: #10b981;">{prediction['method']}</div>
                    <div class="metric-label">Method Used</div>
                </div>''', unsafe_allow_html=True)

            # Year-wise prediction
            st.markdown('<div class="section-header"><div class="section-icon">📊</div><h3>Year-wise Predictions</h3></div>', unsafe_allow_html=True)

            pred_df = pd.DataFrame({
                'Year': [f"Year {i+1}" for i in range(years_ahead)],
                'Predicted Income': prediction['future_incomes'],
                'Estimated Tax': prediction['future_taxes'],
                'Effective Rate (%)': prediction['effective_rates']
            })

            for _, row in pred_df.iterrows():
                st.markdown(f'''<div style="background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                        <div style="flex: 1; min-width: 150px;">
                            <div style="color: #94a3b8; font-size: 0.85rem;">📅 {row['Year']}</div>
                            <div style="color: #f8fafc; font-size: 1.1rem; font-weight: 600; margin-top: 0.25rem;">Income: {format_currency(row['Predicted Income'])}</div>
                        </div>
                        <div style="flex: 1; min-width: 150px; text-align: center;">
                            <div style="color: #94a3b8; font-size: 0.85rem;">💰 Tax Liability</div>
                            <div style="color: #ef4444; font-size: 1.1rem; font-weight: 600; margin-top: 0.25rem;">{format_currency(row['Estimated Tax'])}</div>
                        </div>
                        <div style="flex: 1; min-width: 150px; text-align: right;">
                            <div style="color: #94a3b8; font-size: 0.85rem;">📈 Effective Rate</div>
                            <div style="color: #f59e0b; font-size: 1.1rem; font-weight: 600; margin-top: 0.25rem;">{row['Effective Rate (%)']:.2f}%</div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

            # Trend visualization
            st.markdown('<div class="section-header"><div class="section-icon">📈</div><h3>Income & Tax Trend</h3></div>', unsafe_allow_html=True)

            all_years = [f"H-{len(historical_incomes)-i}" for i in range(len(historical_incomes))] + [f"F+{i+1}" for i in range(years_ahead)]
            all_incomes = historical_incomes + prediction['future_incomes']
            historical_taxes = [st.session_state.lstm_predictor.calculate_tax(inc) for inc in historical_incomes]
            all_taxes = historical_taxes + prediction['future_taxes']

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=all_years[:len(historical_incomes)],
                y=all_incomes[:len(historical_incomes)],
                name='Historical Income',
                line=dict(color='#6366f1', width=3),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=all_years[len(historical_incomes)-1:],
                y=all_incomes[len(historical_incomes)-1:],
                name='Predicted Income',
                line=dict(color='#10b981', width=3, dash='dash'),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=all_years[:len(historical_incomes)],
                y=all_taxes[:len(historical_incomes)],
                name='Historical Tax',
                line=dict(color='#f59e0b', width=2),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=all_years[len(historical_incomes)-1:],
                y=all_taxes[len(historical_incomes)-1:],
                name='Predicted Tax',
                line=dict(color='#ef4444', width=2, dash='dash'),
                mode='lines+markers'
            ))

            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(title='Year', gridcolor='rgba(51, 65, 85, 0.5)'),
                yaxis=dict(title='Amount (₹)', gridcolor='rgba(51, 65, 85, 0.5)')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Recommendations
            st.markdown('<div class="section-header"><div class="section-icon">💡</div><h3>Tax Planning Recommendations</h3></div>', unsafe_allow_html=True)

            recommendations = [
                f"Your tax liability is expected to increase by {format_currency(prediction['future_taxes'][-1] - historical_taxes[-1])} over {years_ahead} years",
                f"Consider maximizing tax-saving investments (80C, 80D, NPS) to reduce tax burden",
                f"With average effective rate of {avg_effective_rate:.1f}%, strategic planning can save significant amounts",
                f"Review your investment portfolio quarterly to align with income growth"
            ]

            for i, rec in enumerate(recommendations, 1):
                st.markdown(f'''<div style="background: var(--surface); border-left: 3px solid #6366f1; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;">
                    <div style="color: #f8fafc;"><strong>{i}.</strong> {rec}</div>
                </div>''', unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown('''<div class="footer">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💰</div>
    <div>Built with ❤️ using Streamlit | <strong>Tax Saver AI v2.0</strong> © 2025</div>
    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #64748b;">Disclaimer: This tool provides estimates only. Please consult a tax professional.</div>
</div>''', unsafe_allow_html=True)
