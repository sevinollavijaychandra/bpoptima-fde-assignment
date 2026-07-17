# BPOptima Forward Deployed Engineer (FDE) Prototype - India Edition

## 1. Architectural Strategy
The GroundSet engine prototype is designed to bridge the gap between unstructured data ingestion and strict, deterministic enterprise rules for the Indian financial sector. The architecture strictly separates the probabilistic "Reader" (AI/LLM) from the deterministic "Judge" (Rule Engine).

- **The LLM Extraction Layer (Simulated):** To maintain prototype accessibility, the LLM layer is simulated using Python Regex heuristics targeting Indian data formats (e.g., INR formatting, CIBIL scores). 
- **The Deterministic Rule Engine:** Once data is extracted, the logic shifts entirely to hard-coded, client-owned deterministic math calculating the Fixed Obligation to Income Ratio (FOIR) against absolute CIBIL thresholds.
- **Separation of Concerns (Codebase):** UI styling and custom HTML/CSS components are completely isolated into a dedicated `style.css` file. This ensures the core Python logic (`app.py` & `engine.py`) remains exceptionally clean, modular, and scalable for production environments.

## 2. Stakeholder Value Alignment
- **Chief Risk Officer (CRO):** The separation of AI extraction and the rules engine guarantees deterministic outcomes. The immutable audit trail and explicit `YES`/`NO` boolean logging eliminate "black box" unpredictability, ensuring full RBI/regulatory compliance.
- **CTO / Enterprise Engineers:** The pipeline demonstrates a clean transformation from raw text into machine-readable `pandas` dataframes, ready for downstream API integration. 

## 3. Advanced Tiered Routing (Case Study)
Beyond simple binary (Pass/Fail) logic, the system introduces a tiered routing mechanism (`APPROVED`, `MANUAL REVIEW`, `REJECTED`) to maximize business conversion without compromising risk parameters. 

**Scenario Evaluation: Rahul Sharma**
- **Extracted Data:** Income: ₹1,20,000 | EMI: ₹55,000 | CIBIL: 730
- **Thresholds:** Minimum CIBIL: 750 | Maximum FOIR: 50%
- **Logic Execution:** The FOIR is healthy at 45.83% (Passes rule), but the CIBIL score of 730 falls marginally short of the 750 threshold (Fails rule).
- **System Outcome:** A basic system would issue a hard `REJECTED` status, losing potential business. Instead, the deterministic engine calculates the marginal variance and safely routes the application to `MANUAL REVIEW`. This forces a human-in-the-loop validation, proving the engine respects hard risk boundaries while protecting business opportunities.