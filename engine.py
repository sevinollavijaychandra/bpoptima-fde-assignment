import re


def extract_entities_from_text(text):
    """
    Simulates an LLM parsing unstructured Indian loan application text.
    Extracts Income, EMI, and CIBIL Score.
    """
    data = {
        "Applicant_Name": "Unknown",
        "Monthly_Income_INR": 0,
        "Monthly_EMI_INR": 0,
        "CIBIL_Score": 0
    }
    
    name_match = re.search(r"Name:\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if name_match: data["Applicant_Name"] = name_match.group(1).strip()
        
    # Matches ₹, Rs, or INR
    income_match = re.search(r"Income:\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)", text, re.IGNORECASE)
    if income_match: data["Monthly_Income_INR"] = int(income_match.group(1).replace(",", ""))
        
    emi_match = re.search(r"(?:EMI|Debt):\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)", text, re.IGNORECASE)
    if emi_match: data["Monthly_EMI_INR"] = int(emi_match.group(1).replace(",", ""))
        
    cibil_match = re.search(r"(?:CIBIL|Score):\s*(\d{3})", text, re.IGNORECASE)
    if cibil_match: data["CIBIL_Score"] = int(cibil_match.group(1))
        
    return data

def run_decision_engine(structured_data, min_cibil, max_foir):
    """
    Applies deterministic Indian banking rules.
    Outputs strict YES/NO boolean logic for executive reporting.
    """
    # ఇక్కడే ఎర్రర్ వచ్చింది. ఇప్పుడు కరెక్ట్ కీస్ (INR) సెట్ చేయబడ్డాయి.
    income = structured_data["Monthly_Income_INR"]
    emi = structured_data["Monthly_EMI_INR"]
    cibil = structured_data["CIBIL_Score"]
    
    # Calculate FOIR (Fixed Obligation to Income Ratio)
    foir = (emi / income * 100) if income > 0 else 100
    
    # Absolute Boolean Checks
    cibil_pass_bool = cibil >= min_cibil
    foir_pass_bool = foir <= max_foir
    
    # String format for executive dashboards
    cibil_pass_str = "YES" if cibil_pass_bool else "NO"
    foir_pass_str = "YES" if foir_pass_bool else "NO"
    
    # Indian Tiered Logic Matrix
    if cibil_pass_bool and foir_pass_bool:
        decision = "APPROVED"
        risk_level = "LOW"
    elif cibil >= (min_cibil - 30) and foir <= (max_foir + 15):
        # Marginal failure (e.g., CIBIL is slightly less, or FOIR is slightly high)
        decision = "MANUAL REVIEW"
        risk_level = "MEDIUM"
    else:
        decision = "REJECTED"
        risk_level = "HIGH"
        
    # Risk Score (0-100)
    cibil_health = min((cibil / min_cibil) * 50, 50)
    foir_health = min((max_foir / foir) * 50, 50) if foir > 0 else 50
    risk_score = round(cibil_health + foir_health, 1)
    
    return {
        "foir_calculated": round(foir, 2),
        "cibil_check": cibil_pass_str,
        "foir_check": foir_pass_str,
        "decision": decision,
        "risk_level": risk_level,
        "risk_score_metric": risk_score
    }