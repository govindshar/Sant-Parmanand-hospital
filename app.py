import streamlit as st
import requests

st.set_page_config(page_title="AI Diagnostic Assistant", layout="centered")

# Header
st.markdown("""
# 🔬 AI Diagnostic Assistant  
**Sant Parmanand Hospital**  
_Supervised by Dr. Amin Jain_

---
""")

st.markdown("## 🧪 Enter Your Lab Test Results")

# Input form
with st.form("lab_form"):
    col1, col2 = st.columns(2)

    with col1:
        hemoglobin = st.text_input("Hemoglobin (g/dL)")
        wbc = st.text_input("WBC (/µL)")
        platelets = st.text_input("Platelets (/µL)")
        ldl = st.text_input("LDL (mg/dL)")
        hdl = st.text_input("HDL (mg/dL)")
        triglycerides = st.text_input("Triglycerides (mg/dL)")
        creatinine = st.text_input("Creatinine (mg/dL)")
        uric_acid = st.text_input("Uric Acid (mg/dL)")

    with col2:
        tsh = st.text_input("TSH (µIU/mL)")
        t3 = st.text_input("T3 (ng/mL)")
        t4 = st.text_input("T4 (µg/dL)")
        alt = st.text_input("ALT (U/L)")
        ast = st.text_input("AST (U/L)")
        bilirubin = st.text_input("Bilirubin (mg/dL)")
        protein = st.selectbox("Protein in Urine", ["", "Present", "Absent"])
        rbc = st.text_input("RBC in Urine (e.g. 0-1/hpf)")

    submitted = st.form_submit_button("🔍 Analyze Report")

# Risk checking
def get_risks(data):
    risks = []
    if data.get("Hemoglobin", 999) < 12: risks.append("Low Hemoglobin – anemia risk")
    if data.get("WBC", 0) > 11000: risks.append("High WBC – infection risk")
    if data.get("Platelets", 999999) < 150000: risks.append("Low Platelets – bleeding risk")
    if data.get("LDL", 0) > 160: risks.append("High LDL – cardiovascular risk")
    if data.get("HDL", 999) < 40: risks.append("Low HDL – poor cholesterol profile")
    if data.get("Triglycerides", 0) > 150: risks.append("High Triglycerides – metabolic risk")
    if data.get("TSH", 0) > 5: risks.append("High TSH – hypothyroidism risk")
    if data.get("TSH", 999) < 0.3: risks.append("Low TSH – hyperthyroidism risk")
    if data.get("ALT", 0) > 55: risks.append("High ALT – liver damage")
    if data.get("AST", 0) > 45: risks.append("High AST – liver inflammation")
    if data.get("Bilirubin", 0) > 1.2: risks.append("High Bilirubin – jaundice risk")
    if data.get("Creatinine", 0) > 1.3: risks.append("High Creatinine – kidney function risk")
    if data.get("Uric Acid", 0) > 7: risks.append("High Uric Acid – gout or kidney risk")
    if protein.lower() == "present": risks.append("Protein in urine – kidney issue")
    if "3" in rbc: risks.append("RBC in urine – infection or bleeding risk")
    return risks

# On submit
if submitted:
    # Clean and convert
    def parse_float(val):
        try: return float(val)
        except: return None

    inputs = {
        "Hemoglobin": parse_float(hemoglobin),
        "WBC": parse_float(wbc),
        "Platelets": parse_float(platelets),
        "LDL": parse_float(ldl),
        "HDL": parse_float(hdl),
        "Triglycerides": parse_float(triglycerides),
        "TSH": parse_float(tsh),
        "T3": parse_float(t3),
        "T4": parse_float(t4),
        "ALT": parse_float(alt),
        "AST": parse_float(ast),
        "Bilirubin": parse_float(bilirubin),
        "Creatinine": parse_float(creatinine),
        "Uric Acid": parse_float(uric_acid),
        "Protein": protein,
        "RBC": rbc
    }

    risks = get_risks(inputs)

    st.markdown("### 📊 AI-Powered Analysis in Progress...")

    # Send to Groq
    prompt = f"""
A patient has submitted lab results:

{inputs}

Based on system-detected risk flags:
{risks}

Please include:
1. Abnormal Test Values – explain in plain language.
2. Risk Assessment – what conditions may arise.
3. Probable Diagnoses.
4. Likely Symptoms.
5. Next Steps for the patient.

Use clear medical tone. Structure it professionally.
"""

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.markdown("### 🩺 Diagnosis Report")
        st.markdown(reply)
    else:
        st.error("❌ Failed to get diagnosis.")
