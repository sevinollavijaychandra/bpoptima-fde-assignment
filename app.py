import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
from engine import extract_entities_from_text, run_decision_engine

st.set_page_config(layout="wide", page_title="BPOptima India FDE", page_icon="🏦")

# ==========================================
# EXTERNAL CSS LOADING FUNCTION
# ==========================================
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading File
local_css("style.css")

# ==========================================
# HEADER & UI COMPONENTS
# ==========================================
st.title("GroundSet India: Deterministic Decision Engine")
st.markdown("**Enterprise system of record for converting unstructured financial evidence into auditable outcomes.**")
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Bank Rule Configuration")
st.sidebar.markdown("Strict logic thresholds that govern final decisions.")
min_cibil = st.sidebar.number_input("Minimum CIBIL Score", min_value=300, max_value=900, value=750)
max_foir = st.sidebar.slider("Maximum Allowable FOIR / EMI Ratio (%)", 10, 80, 50)

st.subheader("1. Evidence Ingestion Module")
tab1, tab2 = st.tabs(["📄 AI Document Extractor", "✍️ Manual Override Form"])

structured_data = None
extraction_method = ""

with tab1:
    default_text = "Applicant Name: Rahul Sharma\nReported Monthly Income: ₹ 1,20,000\nTotal Monthly EMI: ₹ 55,000\nVerified CIBIL Score: 730\nEmployment: TCS - Full Time"
    raw_input = st.text_area("Unstructured Document Text:", value=default_text, height=130)
    
    if st.button("Extract & Run Rules (AI Mode)", type="primary"):
        with st.spinner("Extracting entities via LLM heuristics..."):
            time.sleep(1)
            structured_data = extract_entities_from_text(raw_input)
            extraction_method = "AI_EXTRACTOR"

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        manual_name = st.text_input("Applicant Name", value="Rahul Sharma")
        manual_income = st.number_input("Monthly Income (₹)", min_value=0, value=120000)
    with col_b:
        manual_emi = st.number_input("Monthly EMI (₹)", min_value=0, value=55000)
        manual_score = st.number_input("CIBIL Score", min_value=300, max_value=900, value=730)
        
    if st.button("Run Rules (Manual Mode)"):
        with st.spinner("Processing structured inputs..."):
            time.sleep(0.5)
            structured_data = {
                "Applicant_Name": manual_name,
                "Monthly_Income_INR": manual_income,
                "Monthly_EMI_INR": manual_emi,
                "CIBIL_Score": manual_score
            }
            extraction_method = "MANUAL_ENTRY"

if structured_data is not None:
    results = run_decision_engine(structured_data, min_cibil, max_foir)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("2. Structured Matrix & Logic Verification")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Extracted Machine-Readable Matrix:**")
        st.dataframe(pd.DataFrame([structured_data]), use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("**Deterministic Logic Execution:**")
        st.dataframe(pd.DataFrame([{
            "CIBIL_Threshold_Met": results["cibil_check"],
            "FOIR_Threshold_Met": results["foir_check"]
        }]), use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("3. Final Settlement & Risk Analytics")
    
    out_col1, out_col2, out_col3 = st.columns([1, 1, 2])
    
    with out_col1:
        st.markdown(f"""
        <div class='saas-card'>
            <div class='metric-label'>Calculated FOIR (EMI Ratio)</div>
            <div class='metric-value'>{results['foir_calculated']}%</div>
            <div style='color: #64748b; font-size: 0.8rem;'>Limit: {max_foir}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with out_col2:
        decision = results["decision"]
        if decision == "APPROVED": badge_html = f"<div class='badge badge-approved'>✅ {decision}</div>"
        elif decision == "MANUAL REVIEW": badge_html = f"<div class='badge badge-review'>⚠️ {decision}</div>"
        else: badge_html = f"<div class='badge badge-rejected'>❌ {decision}</div>"
            
        st.markdown(f"""
        <div class='saas-card'>
            <div class='metric-label'>System Outcome</div>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)
        
    with out_col3:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = results["risk_score_metric"],
            title = {'text': "System Confidence / Risk Score", 'font': {'size': 14, 'color': '#64748b'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1e293b"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 40], 'color': "#fee2e2"},
                    {'range': [40, 70], 'color': "#fef3c7"},
                    {'range': [70, 100], 'color': "#d1fae5"}
                ]
            }
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "Inter, sans-serif"})
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("4. Immutable Audit Trail")
    log_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_trail = f"[{log_ts}][{extraction_method}] Financial data mapped and schema verified.\n[{log_ts}][RULE_EVAL] Logic Gate 1: CIBIL Score ({structured_data['CIBIL_Score']}) >= {min_cibil} -> {results['cibil_check']}\n[{log_ts}][RULE_EVAL] Logic Gate 2: Calculated FOIR ({results['foir_calculated']}%) <= {max_foir}% -> {results['foir_check']}\n[{log_ts}][SYSTEM_OUTCOME] Pipeline execution terminated. State routed to: {results['decision']}."
    
    st.code(audit_trail, language="shell")