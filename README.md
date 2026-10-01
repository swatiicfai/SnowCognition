# SnowCognition: Patient 360 & Regulatory Copilot

## Overview
Care and life sciences teams work across siloed EHR and claims data and dense unstructured documents. **SnowCognition** is a Copilot built on Snowflake that unifies this data into a comprehensive Patient 360 dashboard. It answers clinical, safety, and regulatory questions with cited evidence.

This project was built using **100% synthetic/de-identified data** to ensure data privacy and compliance.

### Key Features
*   **Unified Data:** Combines structured patient records (Conditions, Medications) with unstructured clinical notes and FDA regulatory guidelines.
*   **Evidence-Based AI:** Produces cited answers and risk stratification—never opaque predictions.
*   **Interactive UI:** A Streamlit dashboard offering a side-by-side view of the Patient 360 profile and a conversational AI Copilot.

## Architecture
*   **Data Storage:** Snowflake Database (`HEALTHCARE_COPILOT`)
*   **Structured Data:** Snowflake Tables (Patients, Conditions, Medications)
*   **Unstructured Data:** Snowflake Internal Stages (Clinical Notes, Regulatory PDFs/Text)
*   **User Interface:** Python Streamlit

## Judging Focus
1.  **Real World Relevance:** Solves the real-world problem of Care Managers missing critical medication contraindications buried in dense regulatory text.
2.  **Technical Execution:** Seamlessly joins relational data with unstructured text using a Streamlit frontend connected directly to Snowflake.
3.  **Solution Completeness:** Delivers an end-to-end experience from data ingestion to an interactive Q&A Copilot.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/swatiicfai/SnowCognition.git
   cd SnowCognition
   ```

2. **Install requirements:**
   ```bash
   pip install streamlit snowflake-connector-python pandas
   ```

3. **Run the App:**
   ```bash
   streamlit run app.py
   ```
   *(Enter your Snowflake credentials in the sidebar to connect to the database).*
