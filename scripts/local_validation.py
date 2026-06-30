"""Run local validation checks using pandas.

This lets reviewers validate the migration without needing a Snowflake account.
"""
from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

legacy = pd.read_csv(DATA_DIR / "legacy_provider_full.csv")
target = pd.read_csv(DATA_DIR / "snowflake_provider_full.csv")
merged = legacy.merge(target, on="provider_id", how="inner", suffixes=("_legacy", "_snowflake"))

checks = {
    "legacy_count": len(legacy),
    "snowflake_count": len(target),
    "missing_providers": len(legacy[~legacy["provider_id"].isin(target["provider_id"])]),
    "duplicate_npi_rows": int(target.duplicated("npi", keep=False).sum()),
    "date_mismatches": int((pd.to_datetime(merged["credential_expiry_date_legacy"]) != pd.to_datetime(merged["credential_expiry_date_snowflake"])).sum()),
    "status_mismatches": int((merged["credential_status_legacy"].fillna("") != merged["credential_status_snowflake"].fillna("")).sum()),
    "null_specialty_names": int(target["specialty_name"].isna().sum()),
    "invalid_zip_codes": int((~target["zip"].astype(str).apply(lambda z: bool(re.match(r"^[0-9]{5}$", z)))).sum()),
}

print("Healthcare Provider Migration Validation Summary")
print("=" * 55)
for key, value in checks.items():
    print(f"{key}: {value}")
