"""Generate synthetic healthcare provider migration datasets.

This script creates a legacy provider dataset and a Snowflake target dataset with
intentional migration issues for validation and reconciliation practice.
"""
from __future__ import annotations

import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

RANDOM_SEED = 42
fake = Faker("en_US")
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SPECIALTIES = [
    ("CARD", "Cardiology"),
    ("DERM", "Dermatology"),
    ("FAMP", "Family Practice"),
    ("PED", "Pediatrics"),
    ("ORTH", "Orthopedics"),
    ("NEUR", "Neurology"),
    ("ONC", "Oncology"),
    ("PSY", "Psychiatry"),
]
PROVIDER_TYPES = ["MD", "DO", "NP", "PA"]
STATUSES = ["ACTIVE", "INACTIVE", "PENDING"]
STATES = ["CA", "TX", "NY", "FL", "WA", "IL", "AZ", "GA"]


def make_legacy_provider_records(n: int = 500) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        specialty_code, specialty_name = random.choice(SPECIALTIES)
        updated = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))
        expiry = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 730))
        rows.append(
            {
                "provider_id": f"P{i:05d}",
                "npi": str(1000000000 + i),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "provider_type": random.choice(PROVIDER_TYPES),
                "specialty_code": specialty_code,
                "specialty_name": specialty_name,
                "license_number": f"LIC{random.randint(100000, 999999)}",
                "credential_status": random.choices(STATUSES, weights=[80, 15, 5])[0],
                "credential_expiry_date": expiry.date().isoformat(),
                "address_line1": fake.street_address(),
                "city": fake.city(),
                "state": random.choice(STATES),
                "zip": fake.zipcode()[:5],
                "phone": fake.phone_number(),
                "last_updated_date": updated.date().isoformat(),
            }
        )
    return pd.DataFrame(rows)


def make_snowflake_target(legacy: pd.DataFrame) -> pd.DataFrame:
    target = legacy.copy()

    # 1. Missing records: remove 12 providers from target.
    missing_ids = target.sample(12, random_state=1)["provider_id"]
    target = target[~target["provider_id"].isin(missing_ids)].copy()

    # 2. Duplicate NPI: force duplicates on 8 rows.
    duplicate_rows = target.sample(8, random_state=2).index
    target.loc[duplicate_rows, "npi"] = target.iloc[0]["npi"]

    # 3. Credential expiry shifted by one day on 25 rows.
    shifted_rows = target.sample(25, random_state=3).index
    target.loc[shifted_rows, "credential_expiry_date"] = pd.to_datetime(
        target.loc[shifted_rows, "credential_expiry_date"]
    ).dt.date + timedelta(days=1)
    target.loc[shifted_rows, "credential_expiry_date"] = target.loc[
        shifted_rows, "credential_expiry_date"
    ].astype(str)

    # 4. Null specialty names on 18 rows.
    null_specialty_rows = target.sample(18, random_state=4).index
    target.loc[null_specialty_rows, "specialty_name"] = None

    # 5. Invalid ZIP codes on 10 rows.
    bad_zip_rows = target.sample(10, random_state=5).index
    target.loc[bad_zip_rows, "zip"] = "ABCDE"

    # 6. Status drift on 15 rows.
    status_rows = target.sample(15, random_state=6).index
    target.loc[status_rows, "credential_status"] = "ACTIVE"

    # 7. Address formatting differences on 20 rows.
    address_rows = target.sample(20, random_state=7).index
    target.loc[address_rows, "address_line1"] = target.loc[address_rows, "address_line1"].str.upper()

    return target.reset_index(drop=True)


def create_dimension_tables(provider_df: pd.DataFrame, prefix: str) -> None:
    provider_cols = [
        "provider_id",
        "npi",
        "first_name",
        "last_name",
        "provider_type",
        "credential_status",
        "last_updated_date",
    ]
    specialty_cols = ["provider_id", "specialty_code", "specialty_name"]
    location_cols = ["provider_id", "address_line1", "city", "state", "zip", "phone"]
    credential_cols = ["provider_id", "license_number", "credential_status", "credential_expiry_date"]

    provider_df[provider_cols].to_csv(DATA_DIR / f"{prefix}_provider.csv", index=False)
    provider_df[specialty_cols].to_csv(DATA_DIR / f"{prefix}_provider_specialty.csv", index=False)
    provider_df[location_cols].to_csv(DATA_DIR / f"{prefix}_provider_location.csv", index=False)
    provider_df[credential_cols].to_csv(DATA_DIR / f"{prefix}_credentials.csv", index=False)


def main() -> None:
    legacy = make_legacy_provider_records(500)
    snowflake = make_snowflake_target(legacy)

    legacy.to_csv(DATA_DIR / "legacy_provider_full.csv", index=False)
    snowflake.to_csv(DATA_DIR / "snowflake_provider_full.csv", index=False)

    create_dimension_tables(legacy, "legacy")
    create_dimension_tables(snowflake, "snowflake")

    print(f"Created files in {DATA_DIR}")
    print(f"Legacy rows: {len(legacy)}")
    print(f"Snowflake rows: {len(snowflake)}")


if __name__ == "__main__":
    main()
