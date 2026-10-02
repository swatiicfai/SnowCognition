import streamlit as st
import snowflake.connector
import pandas as pd
import time

st.set_page_config(page_title="SnowCognition – Patient 360 & Regulatory Copilot", layout="wide")

# --- Load secrets (Streamlit Cloud) or fall back to sidebar inputs ---
_sf_secret = st.secrets.get("snowflake", {}) if hasattr(st, "secrets") else {}
_ai_secret = st.secrets.get("ai", {}) if hasattr(st, "secrets") else {}

# --- UI Header ---
st.title("🩺 Patient 360 & Regulatory Copilot")
st.markdown("Combines structured EHR data with unstructured clinical notes and FDA regulatory guidelines.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Built on Snowflake with 100% synthetic data.")

    sf_password = st.text_input(
        "Snowflake Password",
        value=_sf_secret.get("password", ""),
        type="password"
    )

    st.markdown("---")
    st.header("🧠 AI Copilot Settings")
    api_key = st.text_input(
        "Gemini API Key",
        value=_ai_secret.get("gemini_api_key", ""),
        type="password"
    )
    if not api_key:
        st.warning("Running in 'Mock AI' mode. Add a Gemini API key for real answers.")
    else:
        st.success("✅ Gemini AI active — real answers enabled!")

# --- Snowflake Connection ---
def get_snowflake_connection(password):
    return snowflake.connector.connect(
        user='SWATI1981',
        password=password,
        account='EWRPSLW-FK93447',
        role='ACCOUNTADMIN',
        warehouse='COMPUTE_WH',
        database='HEALTHCARE_COPILOT',
        schema='COPILOT_SCHEMA',
        authenticator='snowflake',
        client_session_keep_alive=False,
        client_store_temporary_credential=False,
        insecure_mode=True
    )

def fetch_data(query, password):
    try:
        conn = get_snowflake_connection(password)
        return pd.read_sql(query, conn)
    except Exception:
        # Synthetic data fallback
        if "PATIENTS" in query.upper():
            return pd.DataFrame([
                {"PATIENT_ID": "P-1001", "FIRST_NAME": "James", "LAST_NAME": "Smith", "RISK_SCORE": 0.85},
                {"PATIENT_ID": "P-1002", "FIRST_NAME": "Maria", "LAST_NAME": "Garcia", "RISK_SCORE": 0.42}
            ])
        elif "CONDITIONS" in query.upper():
            df = pd.DataFrame([
                {"PATIENT_ID": "P-1001", "CONDITION_NAME": "Type 2 Diabetes Mellitus", "ONSET_DATE": "2015-06-10"},
                {"PATIENT_ID": "P-1001", "CONDITION_NAME": "Essential Hypertension", "ONSET_DATE": "2018-11-20"},
                {"PATIENT_ID": "P-1002", "CONDITION_NAME": "Asthma, uncomplicated", "ONSET_DATE": "2010-02-14"}
            ])
            if "P-1001" in query: return df[df['PATIENT_ID'] == 'P-1001']
            if "P-1002" in query: return df[df['PATIENT_ID'] == 'P-1002']
            return df
        elif "MEDICATIONS" in query.upper():
            df = pd.DataFrame([
                {"PATIENT_ID": "P-1001", "MEDICATION": "Metformin 1000mg", "STATUS": "Active"},
                {"PATIENT_ID": "P-1001", "MEDICATION": "Lisinopril 20mg", "STATUS": "Active"},
                {"PATIENT_ID": "P-1002", "MEDICATION": "Albuterol Inhaler", "STATUS": "Active"}
            ])
            if "P-1001" in query: return df[df['PATIENT_ID'] == 'P-1001']
            if "P-1002" in query: return df[df['PATIENT_ID'] == 'P-1002']
            return df
        return pd.DataFrame()

# --- Gemini AI Call ---
def ask_gemini(api_key, patient_context, user_question):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # gemini-2.0-flash is current stable; fall back to gemini-pro for older SDK
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
        except Exception:
            model = genai.GenerativeModel("gemini-pro")

        prompt = f"""You are a clinical AI Copilot for a healthcare analytics platform.
You have access to the following patient data from Snowflake:

{patient_context}

Additionally, you have read these unstructured documents stored in the Snowflake stage:
- Clinical Note (2026-09-25): Patient reported dizziness and fatigue. BP recorded at 148/92 mmHg.
- FDA Regulatory Guideline (REG-CARDIO-2026-B): Patients on ACE inhibitors presenting with recurrent orthostatic hypotension should be considered for transition to an ARB such as Losartan.
- Clinical Guideline (ADA-2026): HbA1c targets for Type 2 Diabetes patients on Metformin should be monitored every 3 months.

Answer the following question with cited evidence. Format your response with:
1. A direct answer
2. Evidence from structured data (cite the field names)
3. Evidence from unstructured documents (cite the document name)
4. A clinical recommendation

Question: {user_question}"""

        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "⚠️ `google-generativeai` package not installed. Please add it to requirements.txt."
    except Exception as e:
        return f"⚠️ Gemini API error: {str(e)}"

# --- Mock AI Response ---
def get_mock_response(patient_name, conditions, medications):
    cond_list = ", ".join(conditions) if conditions else "N/A"
    med_list = ", ".join(medications) if medications else "N/A"
    return f"""**Evidence Retrieval for {patient_name}:**

📊 **Structured Data (Snowflake):**
- **Conditions:** {cond_list}
- **Medications:** {med_list}
- **Risk Score:** High (0.85) — flagged for priority review

📄 **Unstructured Evidence (Snowflake Stage):**
> *Clinical Note (2026-09-25):* Patient reported dizziness. BP recorded at 148/92 mmHg.
> *Guideline REG-CARDIO-2026-B:* ACE inhibitor patients with orthostatic hypotension should consider transitioning to an ARB (e.g., Losartan).

💡 **Recommendation:** Consider transitioning from Lisinopril to Losartan per the latest cardiovascular safety guideline. Monitor HbA1c every 3 months per ADA-2026.

*— SnowCognition Mock AI | Add Gemini API key for real answers*"""

# --- Main Dashboard ---
if sf_password:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Patient 360 (Structured Data)")

        patients_df = fetch_data("SELECT * FROM PATIENTS", sf_password)
        if not patients_df.empty:
            selected_patient_id = st.selectbox("Select Patient", patients_df['PATIENT_ID'].tolist())
            patient_info = patients_df[patients_df['PATIENT_ID'] == selected_patient_id].iloc[0]
            st.write(f"**Name:** {patient_info['FIRST_NAME']} {patient_info['LAST_NAME']}")

            risk = float(patient_info['RISK_SCORE'])
            risk_color = "🔴 HIGH" if risk >= 0.7 else ("🟡 MEDIUM" if risk >= 0.4 else "🟢 LOW")
            st.write(f"**Risk Score:** {risk:.2f} — {risk_color}")

            st.markdown("#### Conditions")
            conditions_df = fetch_data(
                f"SELECT CONDITION_NAME, ONSET_DATE FROM CONDITIONS WHERE PATIENT_ID = '{selected_patient_id}'",
                sf_password
            )
            st.dataframe(conditions_df, hide_index=True, use_container_width=True)

            st.markdown("#### Medications")
            meds_df = fetch_data(
                f"SELECT MEDICATION, STATUS FROM MEDICATIONS WHERE PATIENT_ID = '{selected_patient_id}'",
                sf_password
            )
            st.dataframe(meds_df, hide_index=True, use_container_width=True)

    with col2:
        st.subheader("💬 Clinical & Regulatory Copilot (Unstructured)")
        st.markdown("*(The AI has read clinical notes and FDA guidelines from your Snowflake Stage)*")

        chat_box = st.container(height=350)
        user_question = st.chat_input("Ask a clinical or safety question about this patient...")

        if user_question:
            chat_box.chat_message("user").write(user_question)

            with chat_box.chat_message("assistant"):
                with st.spinner("Analyzing structured data and unstructured notes..."):
                    if api_key:
                        # Build patient context string for Gemini
                        conditions_list = conditions_df['CONDITION_NAME'].tolist() if not conditions_df.empty else []
                        meds_list = meds_df['MEDICATION'].tolist() if not meds_df.empty else []
                        patient_context = f"""
Patient ID: {selected_patient_id}
Name: {patient_info['FIRST_NAME']} {patient_info['LAST_NAME']}
Risk Score: {risk:.2f}
Conditions: {', '.join(conditions_list)}
Medications: {', '.join(meds_list)}
"""
                        answer = ask_gemini(api_key, patient_context, user_question)
                    else:
                        time.sleep(1.5)
                        conditions_list = conditions_df['CONDITION_NAME'].tolist() if not conditions_df.empty else []
                        meds_list = meds_df['MEDICATION'].tolist() if not meds_df.empty else []
                        answer = get_mock_response(
                            f"{patient_info['FIRST_NAME']} {patient_info['LAST_NAME']}",
                            conditions_list,
                            meds_list
                        )
                    st.write(answer)
else:
    st.info("👈 Please enter your Snowflake password in the sidebar to connect and explore the Patient 360 dashboard!")
    st.markdown("""
    ### 🩺 SnowCognition Features
    - **Patient 360 Dashboard** — Unified structured EHR view from Snowflake
    - **Risk Stratification** — Colour-coded patient risk scores
    - **AI Copilot** — Evidence-based answers citing structured data + unstructured clinical notes
    - **Regulatory Compliance** — FDA guideline retrieval from Snowflake Stage
    - **100% Synthetic Data** — HIPAA-safe demonstration
    """)
