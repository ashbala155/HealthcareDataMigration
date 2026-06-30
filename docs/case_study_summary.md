# Case Study Summary

## Title

Healthcare Provider Data Migration Validation: Legacy Warehouse to Snowflake

## Objective

The objective of this project is to validate whether healthcare provider data was migrated accurately from a legacy source system into a Snowflake target environment.

## Scenario

A healthcare analytics team is migrating provider data into Snowflake. The provider data supports credentialing, provider directories, specialty reporting, claims routing, and network analytics. After migration, the team needs to confirm that the target records match the source records and that any data quality issues are identified before downstream reporting begins.

## Data Domains

The project covers four provider data domains:

1. Provider demographics
2. Provider specialties
3. Provider locations
4. Provider credentials

## Validation Strategy

The validation framework compares source and target data across multiple quality dimensions:

- Completeness
- Uniqueness
- Accuracy
- Consistency
- Validity
- Referential alignment

## Main Checks

| Check | Purpose |
|---|---|
| Row count reconciliation | Confirms overall source-to-target record volume |
| Missing provider check | Finds records dropped during migration |
| Duplicate NPI check | Identifies duplicate provider identifiers |
| Credential expiry date check | Detects date conversion or timezone drift |
| Specialty null check | Finds incomplete specialty mappings |
| ZIP code validation | Flags invalid provider location records |
| Status mismatch check | Finds business rule transformation issues |
| Address drift check | Detects formatting changes |

## Findings from Synthetic Dataset

The migrated Snowflake dataset includes intentional defects:

- Some providers are missing from the target system.
- Several NPI values are duplicated.
- Some credential expiry dates shifted by one day.
- Some specialty names are null.
- Some ZIP codes are invalid.
- Some provider credential statuses changed.
- Some addresses were transformed to uppercase.

## Business Impact

These issues could affect:

- Provider directory accuracy
- Credentialing operations
- Claims routing
- Compliance reporting
- Provider network analytics
- Downstream dashboards and executive reporting

## Recommended Remediation

1. Reprocess missing provider records.
2. Enforce NPI uniqueness rules before loading into Snowflake.
3. Review date conversion logic for credential expiry fields.
4. Add specialty code-to-name mapping validation.
5. Apply ZIP code format validation before target load.
6. Align provider status transformation rules with business definitions.
7. Standardize address formatting rules and document acceptable transformations.

## Final Outcome

This project demonstrates an end-to-end healthcare provider migration validation workflow using SQL, Python, Pandas, and Streamlit. It is designed to show practical data analyst skills in healthcare data quality, migration reconciliation, Snowflake validation, and stakeholder reporting.
