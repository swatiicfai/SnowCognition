import os
import csv

# Setup directories
base_dir = r"C:\Users\Swati\.gemini\antigravity\scratch\snowflake_copilot_project\data"
structured_dir = os.path.join(base_dir, "structured")
unstructured_dir = os.path.join(base_dir, "unstructured")
os.makedirs(structured_dir, exist_ok=True)
os.makedirs(unstructured_dir, exist_ok=True)

# ==========================================
# 1. STRUCTURED DATA (Mock EHR/Claims)
# ==========================================
patients = [
    {"patient_id": "P-1001", "first_name": "James", "last_name": "Smith", "dob": "1958-04-12", "gender": "M", "risk_score": 0.85},
    {"patient_id": "P-1002", "first_name": "Maria", "last_name": "Garcia", "dob": "1975-08-22", "gender": "F", "risk_score": 0.42}
]

conditions = [
    {"patient_id": "P-1001", "condition_code": "E11.9", "condition_name": "Type 2 Diabetes Mellitus", "onset_date": "2015-06-10"},
    {"patient_id": "P-1001", "condition_code": "I10", "condition_name": "Essential Hypertension", "onset_date": "2018-11-20"},
    {"patient_id": "P-1002", "condition_code": "J45.909", "condition_name": "Asthma, uncomplicated", "onset_date": "2010-02-14"}
]

medications = [
    {"patient_id": "P-1001", "medication": "Metformin 1000mg", "status": "Active", "last_fill_date": "2026-08-01"},
    {"patient_id": "P-1001", "medication": "Lisinopril 20mg", "status": "Active", "last_fill_date": "2026-08-01"},
    {"patient_id": "P-1002", "medication": "Albuterol Inhaler", "status": "Active", "last_fill_date": "2026-09-15"}
]

# Write CSVs
for name, data in [("patients.csv", patients), ("conditions.csv", conditions), ("medications.csv", medications)]:
    with open(os.path.join(structured_dir, name), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# ==========================================
# 2. UNSTRUCTURED DATA (Clinical Notes)
# ==========================================
note_p1001 = """CLINICAL VISIT NOTE
Date: 2026-09-25
Patient: James Smith (P-1001)
Attending: Dr. Sarah Jenkins, Cardiology/Endocrinology

SUBJECTIVE:
Patient presents for routine follow-up of Type 2 Diabetes and Hypertension. Patient reports feeling generally fatigued and notes recent episodes of dizziness when standing up quickly. He admits to occasionally forgetting his evening dose of Lisinopril.

OBJECTIVE:
BP: 145/90 (Elevated)
HR: 78 bpm
HbA1c: 8.2% (Up from 7.5% six months ago)

ASSESSMENT & PLAN:
1. Hypertension: Suboptimally controlled. Dizziness may be orthostatic hypotension related to Lisinopril or dehydration.
2. Type 2 Diabetes: HbA1c is climbing. Metformin adherence seems okay, but dietary habits need review.

Plan: Patient advised to monitor BP at home daily. Schedule follow-up in 4 weeks to consider switching from Lisinopril to Losartan if dizziness persists, pending review of latest cardiovascular safety guidelines for diabetic patients.
"""
with open(os.path.join(unstructured_dir, "clinical_note_P1001_20260925.txt"), 'w') as f:
    f.write(note_p1001)

# ==========================================
# 3. UNSTRUCTURED DATA (Regulatory/Guidelines)
# ==========================================
regulatory_guideline = """CLINICAL & REGULATORY GUIDELINE: HYPERTENSION MANAGEMENT IN DIABETIC PATIENTS (SYNTHETIC)
Document ID: REG-CARDIO-2026-B
Effective Date: 2026-01-01

SUMMARY:
This guideline outlines the recommended pharmacological interventions for adult patients with comorbid Type 2 Diabetes and Hypertension.

KEY RECOMMENDATIONS:
- First-line therapy includes ACE inhibitors (e.g., Lisinopril) or ARBs (e.g., Losartan).
- Safety Warning: Patients on ACE inhibitors presenting with recurrent orthostatic hypotension (dizziness upon standing) should be immediately evaluated for volume depletion.
- If orthostatic hypotension persists and impacts quality of life, it is strongly recommended to discontinue the ACE inhibitor and transition the patient to an ARB (such as Losartan).
- Routine monitoring of renal function (eGFR) and serum potassium is required within 2 weeks of transitioning therapies to an ARB.
"""
with open(os.path.join(unstructured_dir, "guideline_hypertension_diabetes.txt"), 'w') as f:
    f.write(regulatory_guideline)

print(f"✅ Generated synthetic dataset in: {base_dir}")
