from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Healthcare Provider Migration Validation",
    page_icon="🏥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    legacy = pd.read_csv(DATA_DIR / "legacy_provider_full.csv")
    target = pd.read_csv(DATA_DIR / "snowflake_provider_full.csv")
    return legacy, target

legacy, target = load_data()

st.title("Healthcare Provider Data Migration Validation")
st.caption("Synthetic provider migration case study: legacy warehouse to Snowflake target validation and reconciliation")

legacy_count = len(legacy)
target_count = len(target)
missing = legacy[~legacy["provider_id"].isin(target["provider_id"])]
duplicate_npis = target[target.duplicated("npi", keep=False)].sort_values("npi")

merged = legacy.merge(target, on="provider_id", how="inner", suffixes=("_legacy", "_snowflake"))

expiry_mismatch = merged[
    pd.to_datetime(merged["credential_expiry_date_legacy"])
    != pd.to_datetime(merged["credential_expiry_date_snowflake"])
].copy()
expiry_mismatch["date_difference_days"] = (
    pd.to_datetime(expiry_mismatch["credential_expiry_date_snowflake"])
    - pd.to_datetime(expiry_mismatch["credential_expiry_date_legacy"])
).dt.days

status_mismatch = merged[
    merged["credential_status_legacy"].fillna("")
    != merged["credential_status_snowflake"].fillna("")
]

null_specialty = target[target["specialty_name"].isna() | (target["specialty_name"].astype(str).str.strip() == "")]
invalid_zip = target[~target["zip"].astype(str).apply(lambda z: bool(re.match(r"^[0-9]{5}$", z)))]
address_case_drift = merged[
    (merged["address_line1_legacy"].fillna("") != merged["address_line1_snowflake"].fillna(""))
    & (merged["address_line1_legacy"].fillna("").str.upper() == merged["address_line1_snowflake"].fillna("").str.upper())
]

issue_summary = pd.DataFrame(
    {
        "Check": [
            "Row Count Difference",
            "Missing Providers",
            "Duplicate NPI Rows",
            "Credential Date Mismatches",
            "Status Mismatches",
            "Null Specialty Names",
            "Invalid ZIP Codes",
            "Address Case Drift",
        ],
        "Issue Count": [
            abs(legacy_count - target_count),
            len(missing),
            len(duplicate_npis),
            len(expiry_mismatch),
            len(status_mismatch),
            len(null_specialty),
            len(invalid_zip),
            len(address_case_drift),
        ],
    }
)

accuracy = round((len(merged) - issue_summary["Issue Count"].sum()) / max(len(legacy), 1) * 100, 2)
accuracy = max(0, accuracy)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Legacy Records", f"{legacy_count:,}")
col2.metric("Snowflake Records", f"{target_count:,}")
col3.metric("Missing Records", f"{len(missing):,}")
col4.metric("Estimated Accuracy", f"{accuracy}%")

st.divider()

left, right = st.columns([1, 1])
with left:
    st.subheader("Reconciliation Issue Summary")
    st.dataframe(issue_summary, use_container_width=True)

with right:
    st.subheader("Issue Counts by Validation Check")
    fig = px.bar(issue_summary, x="Check", y="Issue Count", text="Issue Count")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Provider Records by Specialty")
specialty_counts = target["specialty_name"].fillna("Missing Specialty").value_counts().reset_index()
specialty_counts.columns = ["Specialty", "Provider Count"]
fig2 = px.pie(specialty_counts, names="Specialty", values="Provider Count")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Exception Detail Tables")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Missing Providers",
    "Duplicate NPIs",
    "Date Mismatches",
    "Null Specialties",
    "Invalid ZIPs",
])

with tab1:
    st.dataframe(missing, use_container_width=True)
with tab2:
    st.dataframe(duplicate_npis, use_container_width=True)
with tab3:
    display_cols = [
        "provider_id",
        "npi_legacy",
        "first_name_legacy",
        "last_name_legacy",
        "credential_expiry_date_legacy",
        "credential_expiry_date_snowflake",
        "date_difference_days",
    ]
    st.dataframe(expiry_mismatch[display_cols], use_container_width=True)
with tab4:
    st.dataframe(null_specialty, use_container_width=True)
with tab5:
    st.dataframe(invalid_zip, use_container_width=True)

st.divider()
st.subheader("Business Interpretation")
st.write(
    """
This dashboard simulates the validation layer of a healthcare provider data migration.
The most important migration risks are missing provider records, duplicate NPIs, credentialing date drift,
invalid location fields, and specialty mapping gaps. These issues can affect downstream provider directories,
credentialing workflows, network adequacy reporting, claims routing, and analytics accuracy.
"""
)
