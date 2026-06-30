# Healthcare Provider Data Migration Case Study

A portfolio-ready healthcare data migration project that simulates moving provider data from a legacy warehouse into a Snowflake target environment, then validating and reconciling the migrated records.

## Project Summary

This case study demonstrates how provider data can be validated after migration from a legacy system to Snowflake. The project uses synthetic healthcare provider data and intentionally introduces common migration issues such as missing records, duplicate NPIs, date drift, null specialty mappings, invalid ZIP codes, and status mismatches.

## Business Problem

Healthcare organizations rely on accurate provider data for credentialing, provider directories, claims routing, compliance reporting, and network analytics. During migration from a legacy warehouse to Snowflake, data quality issues can appear because of schema changes, transformation logic, date conversions, null handling, or incomplete mappings.

This project answers the question:

> Did all provider records migrate completely and accurately into Snowflake?

## Key Features

- Synthetic provider dataset with 500 legacy records
- Simulated Snowflake target dataset with intentional migration defects
- SQL scripts for Snowflake table creation and validation
- Python-based local validation script
- Streamlit dashboard for reconciliation reporting
- Exception detail views for missing records, duplicate NPIs, date mismatches, null specialties, and invalid ZIP codes

## Tech Stack

- SQL
- Snowflake
- Python
- Pandas
- Streamlit
- Plotly
- Faker
- Data Validation
- Healthcare Provider Data

## Folder Structure

```text
healthcare-data-migration-case-study/
│
├── data/
│   ├── legacy_provider_full.csv
│   ├── snowflake_provider_full.csv
│   ├── legacy_provider.csv
│   ├── snowflake_provider.csv
│   ├── legacy_provider_specialty.csv
│   ├── snowflake_provider_specialty.csv
│   ├── legacy_provider_location.csv
│   ├── snowflake_provider_location.csv
│   ├── legacy_credentials.csv
│   └── snowflake_credentials.csv
│
├── dashboard/
│   └── app.py
│
├── scripts/
│   ├── generate_synthetic_data.py
│   └── local_validation.py
│
├── sql/
│   ├── create_tables.sql
│   ├── load_csv_stage_example.sql
│   ├── validation_checks.sql
│   └── reconciliation_summary.sql
│
├── docs/
│   └── case_study_summary.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/healthcare-data-migration-case-study.git
cd healthcare-data-migration-case-study
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Regenerate synthetic data, optional

```bash
python scripts/generate_synthetic_data.py
```

### 5. Run local validation

```bash
python scripts/local_validation.py
```

### 6. Run the dashboard

```bash
streamlit run dashboard/app.py
```

## Validation Checks Included

### 1. Row Count Reconciliation

Compares the number of records in the legacy provider table against the Snowflake target table.

### 2. Missing Provider Records

Identifies providers that exist in the legacy source but do not exist in the Snowflake target.

### 3. Duplicate NPI Check

Detects duplicate National Provider Identifier values in the Snowflake target table.

### 4. Credential Expiry Date Mismatch

Finds credential expiry dates that shifted during migration.

### 5. Specialty Mapping Gaps

Identifies providers whose specialty names are missing after migration.

### 6. Invalid ZIP Code Check

Flags provider location records with invalid ZIP code formats.

### 7. Provider Status Drift

Compares credential status values between legacy and Snowflake records.

### 8. Address Formatting Drift

Detects address fields that changed because of formatting or case transformations.

## Example SQL Validation Query

```sql
SELECT
    L.PROVIDER_ID,
    L.CREDENTIAL_EXPIRY_DATE AS LEGACY_EXPIRY_DATE,
    S.CREDENTIAL_EXPIRY_DATE AS SNOWFLAKE_EXPIRY_DATE,
    DATEDIFF('day', L.CREDENTIAL_EXPIRY_DATE, S.CREDENTIAL_EXPIRY_DATE) AS DATE_DIFFERENCE_DAYS
FROM LEGACY_CREDENTIALS L
JOIN SNOWFLAKE_CREDENTIALS S
    ON L.PROVIDER_ID = S.PROVIDER_ID
WHERE L.CREDENTIAL_EXPIRY_DATE <> S.CREDENTIAL_EXPIRY_DATE;
```

## Simulated Migration Issues

The target Snowflake dataset intentionally includes:

- 12 missing provider records
- Duplicate NPI values
- Credential expiry dates shifted by 1 day
- Null specialty names
- Invalid ZIP codes
- Credential status mismatches
- Address formatting drift

## Dashboard Preview

The Streamlit dashboard includes:

- Legacy record count
- Snowflake record count
- Missing record count
- Estimated migration accuracy
- Issue counts by validation check
- Provider distribution by specialty
- Detailed exception tables

## Portfolio Description

**Healthcare Provider Data Migration Validation: Legacy Warehouse to Snowflake**

Built a healthcare provider data migration validation framework to compare legacy warehouse records against a Snowflake target dataset. Developed SQL reconciliation checks for row counts, missing providers, duplicate NPIs, credential expiry date mismatches, specialty mapping gaps, invalid ZIP codes, and provider status drift. Created a Streamlit dashboard to summarize migration quality and exception trends for business and technical stakeholders.

## Resume Bullets

- Designed a Snowflake-based validation framework for healthcare provider data migration using SQL, Python, and Pandas.
- Built reconciliation checks for row counts, missing records, duplicate NPIs, date mismatches, null specialty mappings, and invalid ZIP codes.
- Developed a Streamlit dashboard to monitor migration accuracy, exception counts, and provider-level validation failures.
- Documented root causes of migration drift including schema mapping gaps, date conversion issues, inconsistent null handling, and formatting transformations.

## Disclaimer

This project uses fully synthetic provider data generated for portfolio and educational purposes. It does not contain real patient, provider, PHI, or HIPAA-regulated data.
