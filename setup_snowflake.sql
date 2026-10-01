-- ==========================================
-- SNOWFLAKE SETUP SCRIPT: HEALTHCARE COPILOT
-- ==========================================

-- 1. Create Database and Schema
CREATE DATABASE IF NOT EXISTS HEALTHCARE_COPILOT;
USE DATABASE HEALTHCARE_COPILOT;
CREATE SCHEMA IF NOT EXISTS COPILOT_SCHEMA;
USE SCHEMA COPILOT_SCHEMA;

-- 2. Create Tables for Structured Data
CREATE OR REPLACE TABLE patients (
    patient_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    gender VARCHAR(10),
    risk_score FLOAT
);

CREATE OR REPLACE TABLE conditions (
    patient_id VARCHAR(50),
    condition_code VARCHAR(20),
    condition_name VARCHAR(100),
    onset_date DATE
);

CREATE OR REPLACE TABLE medications (
    patient_id VARCHAR(50),
    medication VARCHAR(100),
    status VARCHAR(20),
    last_fill_date DATE
);

-- 3. Create File Formats & Stages
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  NULL_IF = ('NULL', 'null')
  EMPTY_FIELD_AS_NULL = true;

-- Stage for CSVs
CREATE OR REPLACE STAGE structured_data_stage
  FILE_FORMAT = csv_format;

-- Stage for Unstructured text/PDF files
CREATE OR REPLACE STAGE unstructured_docs_stage
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- ==========================================
-- UPLOAD COMMANDS (Run via SnowSQL CLI)
-- ==========================================
/*
-- Run these from your terminal in the project directory to upload the local files:

snowsql -c your_connection -q "PUT file://data/structured/*.csv @HEALTHCARE_COPILOT.COPILOT_SCHEMA.structured_data_stage AUTO_COMPRESS=FALSE;"
snowsql -c your_connection -q "PUT file://data/unstructured/*.txt @HEALTHCARE_COPILOT.COPILOT_SCHEMA.unstructured_docs_stage AUTO_COMPRESS=FALSE;"
*/

-- ==========================================
-- 4. Ingest Structured Data
-- ==========================================
COPY INTO patients
FROM @structured_data_stage/patients.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
ON_ERROR = 'CONTINUE';

COPY INTO conditions
FROM @structured_data_stage/conditions.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
ON_ERROR = 'CONTINUE';

COPY INTO medications
FROM @structured_data_stage/medications.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
ON_ERROR = 'CONTINUE';

-- Check data
-- SELECT * FROM patients;
