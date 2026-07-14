import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Page configuration for a professional, wide dashboard layout
st.set_page_config(
    layout="wide", 
    page_title="BPOptima GroundSet Engine Prototype",
    initial_sidebar_state="expanded"
)

# App Title & Context
st.title("GroundSet Engine: Automated Trust & Deterministic Decisions")
st.markdown(
    "Verifying evidence transparency by converting unstructured data into audited, client-owned business outcomes."
)
st.divider()

# ==========================================
# SIDEBAR: CLIENT-OWNED DETERMINISTIC RULES
# ==========================================
st.sidebar.header("🛡️ Client Rule Configuration")
st.sidebar.markdown(
    "Define the hard boundaries for the decision engine. These rules are absolute; outcomes cannot be invented."
)

min_credit_score = st.sidebar.slider("Minimum Bureau Credit Score", 500, 850, 710)
max_debt_ratio = st.sidebar.slider("Maximum Allowable Debt-to-Income Ratio (%)", 10, 80, 45)
require_active_employment = st.sidebar.toggle("Require Verifiable Active Employment", value=True)

# ==========================================
# ROW 1: EVIDENCE INGESTION & DATA STRUCTURE
# ==========================================
st.subheader("1. GroundSet Ingestion Pipeline")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### **Unstructured Evidence Ingested**")
    st.caption("Simulated document read (PDF/Image/Scanned Application)")
    
    sample_document = """[DOCUMENT: LOAN_APP_REF_99812]
Applicant Legal Name: Johnathan Doe
Current Monthly Gross Income: $8,500
Declared Monthly Debt Obligations: $3,900
Credit Bureau Pull: 725 Score (Equifax Verified)
Current Employment Status: Active (Senior Logistics Specialist)
Tenure: 4 Years, 2 Months"""
    
    st.text_area("Raw Text Stream", sample_document, height=180, disabled=True)

with col2:
    st.markdown("### **Structured Variables Extracted**")
    st.caption("GroundSet converts raw text streams into machine-ready categorical & numeric values.")
    
    # Feature map reflecting structured data engineering
    extracted_features = {
        "Variable / Feature": ["Applicant Name", "Monthly Income", "Monthly Debt", "Credit Score", "Employment Status"],
        "Extracted Value": ["Johnathan Doe", 85000, 39000, 725, "Active"],
        "Data Type": ["STRING", "INTEGER", "INTEGER", "INTEGER", "CATEGORICAL"]
    }
    df_features = pd.DataFrame(extracted_features)
    st.dataframe(df_features, use_container_width=True, hide_index=True)

st.divider()

# ==========================================
# ROW 2: RULE RUNNER & AUDIT LOG
# ==========================================
st.subheader("2. Deterministic Rule Processing & Verification")

if st.button("Execute GroundSet Decision Engine", type="primary"):
    
    # Compute operational parameters derived from features
    calculated_dti = (39000 / 85000) * 100
    
    # Evaluate explicit boolean logic gates
    credit_pass = 725 >= min_credit_score
    dti_pass = calculated_dti <= max_debt_ratio
    emp_pass = not require_active_employment or (require_active_employment and "Active" == "Active")
    
    final_decision = credit_pass and dti_pass and emp_pass

    # Render simulated step-by-step processing intervals for visual pacing
    with st.spinner("Processing compliance matrices..."):
        time.sleep(0.6)
        
        # Build strict, non-pronoun objective audit logs
        log_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        audit_trail = f"""[{log_ts}][INGESTION] Document stream LOAN_APP_REF_99812 parsed successfully.
[{log_ts}][DATATYPE] Normalizing features: Income -> INT, Debt -> INT, Credit -> INT.
[{log_ts}][RULE_EVAL] Rule 1: Evaluate Bureau Credit Score (725) >= Threshold ({min_credit_score}) -> Result: {str(credit_pass).upper()}
[{log_ts}][RULE_EVAL] Rule 2: Evaluate Calculated Debt-to-Income ({calculated_dti:.2f}%) <= Threshold ({max_debt_ratio}%) -> Result: {str(dti_pass).upper()}
[{log_ts}][RULE_EVAL] Rule 3: Evaluate Employment Status Obligation Requirement ({require_active_employment}) -> Result: {str(emp_pass).upper()}
[{log_ts}][DECISION] Aggregating deterministic evaluation outputs. Zero probabilistic fallback paths triggered."""
        
        st.markdown("#### **Immutable Step-by-Step Audit Trail**")
        st.code(audit_trail, language="shell")
    
    st.markdown("### **3. Final Output & State Settlement**")
    
    out_col1, out_col2 = st.columns([1, 2])
    
    with out_col1:
        st.markdown("**System Decision Result:**")
        if final_decision:
            st.success("🟢 **APPROVED**")
        else:
            st.error("🔴 **REJECTED**")
            
    with out_col2:
        st.markdown("**Structured Data Matrix Output:**")
        final_record = pd.DataFrame([{
            "Credit_Check_Pass": "YES" if credit_pass else "NO",
            "DTI_Check_Pass": "YES" if dti_pass else "NO",
            "Employment_Check_Pass": "YES" if emp_pass else "NO",
            "Deterministic_Settlement": "APPROVED" if final_decision else "REJECTED"
        }])
        st.dataframe(final_record, hide_index=True)
else:
    st.info("Click the button above to execute the pipeline and view the real-time audit logs.")