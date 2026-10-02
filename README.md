# SnowCognition 🩺❄️
### Patient 360 & Regulatory Copilot — CoCo CLI Hackathon GCC Edition

<p align="center">
  <img src="https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  <b>🌐 Live Demo:</b> <a href="https://snowcognition-5pyisfhicsv9xeh4vymvrq.streamlit.app">snowcognition-5pyisfhicsv9xeh4vymvrq.streamlit.app</a>
</p>

---

## 🏆 Hackathon Submission

| | |
|---|---|
| **Event** | Snowflake CoCo CLI Hackathon — GCC Edition |
| **Challenge** | Patient and Member 360 & Clinical / Regulatory Document Copilot |
| **Team** | SnowCognition |
| **Team Leader** | Swati Gupta |
| **Members** | Abhishek Kontharia · ManidharReddy Bheempadu · Swati Gupta |

---

## 🔍 Problem Statement

Care and life-sciences teams work across **siloed EHR/claims data** and dense unstructured documents (clinical notes, FDA guidelines). This leads to:

- ❌ Delayed clinical decisions (hours of manual cross-referencing)
- ❌ Missed safety signals (no unified patient risk view)
- ❌ Regulatory non-compliance (guidelines buried in documents)

---

## ✅ Solution — SnowCognition

A unified **Patient 360 dashboard** + **Evidence-Based AI Copilot** built entirely on Snowflake:

| Feature | Description |
|---|---|
| 📋 **Patient 360** | Unified structured view: conditions, medications, risk score — all from Snowflake |
| 🔴 **Risk Stratification** | Automated colour-coded risk flags (🔴 HIGH / 🟡 MEDIUM / 🟢 LOW) |
| 💬 **AI Copilot** | Gemini 3.8 Flash answers clinical questions with **cited evidence** |
| 📄 **Regulatory Q&A** | FDA guidelines retrieved from Snowflake Stage, surfaced in-context |
| 🔒 **100% Synthetic Data** | HIPAA-safe — all patient data is de-identified and synthetically generated |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│  Synthetic CSVs  ──►  generate_data.py  ──►  Snowflake Tables   │
│  Clinical Notes (TXT) / FDA Guidelines (PDF) ──► Snowflake Stage│
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   ❄️ SNOWFLAKE  │
                    │  HEALTHCARE_    │
                    │  COPILOT DB     │
                    │  COPILOT_SCHEMA │
                    │  Internal Stage │
                    └────────┬────────┘
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼──────────┐      ┌──────────▼──────────┐
    │  📊 STRUCTURED     │      │  📄 UNSTRUCTURED     │
    │  SQL Queries        │      │  Stage Doc Context   │
    │  Patient 360 Data   │      │  ──► Gemini 3.8 Flash│
    └─────────┬──────────┘      └──────────┬──────────┘
              └──────────────┬─────────────┘
                             │
                    ┌────────▼────────┐
                    │  🖥️ STREAMLIT   │
                    │  Patient 360 UI  │
                    │  AI Copilot Chat │
                    │  Risk Dashboard  │
                    └─────────────────┘
```

### CoCo CLI Skills Used
| Skill | Purpose |
|---|---|
| `snowflake-connector-python` | Structured query skill — SQL to Snowflake tables |
| `google-generativeai` | LLM inference skill — Gemini 3.8 Flash for clinical Q&A |
| `streamlit` | UI rendering skill — Patient 360 + Copilot interface |
| `pandas` | Data wrangling skill — DataFrame transformations |
| `Streamlit Secrets` | Credential management skill — secure key injection |

---

## 📁 Project Structure

```
SnowCognition/
├── app.py                         # Main Streamlit application
├── generate_data.py               # Synthetic data generator
├── setup_snowflake.sql            # Snowflake DB/schema/table setup SQL
├── requirements.txt               # Python dependencies
├── .streamlit/
│   ├── config.toml                # Streamlit UI theme configuration
│   └── secrets.toml.example       # Secret keys template (DO NOT commit real secrets)
├── data/
│   ├── structured/
│   │   ├── patients.csv           # Synthetic patient records
│   │   ├── conditions.csv         # Synthetic conditions data
│   │   └── medications.csv        # Synthetic medications data
│   └── unstructured/
│       ├── clinical_note_P1001_20260925.txt    # Synthetic clinical note
│       └── guideline_hypertension_diabetes.txt # Synthetic FDA guideline
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A Snowflake account (free trial at [snowflake.com](https://signup.snowflake.com/))
- A Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/apikey))

### Step 1 — Clone & Install

```bash
git clone https://github.com/swatiicfai/SnowCognition.git
cd SnowCognition
pip install -r requirements.txt
```

### Step 2 — Set Up Snowflake

Run `setup_snowflake.sql` in your Snowflake worksheet to create the database, schema, and tables.

```bash
# Then generate and load synthetic data:
python generate_data.py
```

### Step 3 — Configure Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your credentials:

```toml
[snowflake]
password = "your_snowflake_password"

[ai]
gemini_api_key = "your_gemini_api_key"
```

> ⚠️ **Never commit `secrets.toml`** — it is in `.gitignore`.

### Step 4 — Run

```bash
streamlit run app.py
```

---

## 🌐 Live Deployment

The app is deployed on **Streamlit Community Cloud**:

👉 **[https://snowcognition-5pyisfhicsv9xeh4vymvrq.streamlit.app](https://snowcognition-5pyisfhicsv9xeh4vymvrq.streamlit.app)**

Enter the Snowflake password in the sidebar to connect, or the app will load with built-in synthetic demo data.

---

## 📈 Impact

| Metric | Before | After |
|---|---|---|
| Clinical query time | 2–3 hours | **< 30 seconds** |
| Evidence citation | 0% | **100%** (every answer cited) |
| Risk flagging | Manual | **Automated** (colour-coded) |
| Regulatory lookup | Multi-day | **Real-time in-context** |
| Data privacy | Risk of PHI exposure | **HIPAA-safe** (100% synthetic) |

---

## 🔮 Future Roadmap

- 🏥 Connect to real EHR systems (Epic, Cerner) via Snowflake connectors
- 🔍 Snowflake Cortex Search over full document corpus
- 🧪 Clinical Trial Matching from Patient 360 profiles
- 📡 Real-time patient monitoring via Snowpipe
- 🏢 Snowflake Native App for enterprise one-click deployment

---

## 👥 Team SnowCognition

| Name | Role | Email |
|---|---|---|
| **Swati Gupta** | Team Leader | swati.icfai@rediffmail.com |
| **Abhishek Kontharia** | Developer | abhishek.11111997@gmail.com |
| **ManidharReddy Bheempadu** | Developer | 24br1a0571.manohar@gmail.com |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ for the <b>Snowflake CoCo CLI Hackathon — GCC Edition</b></p>
