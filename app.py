"""Streamlit dashboard for the local, non-destructive migration preview."""
from pathlib import Path
import pandas as pd
import streamlit as st
from hubspot_migration.migration import prepare_contacts

st.set_page_config(page_title="HubSpot Migration Workbench", page_icon="🔄", layout="wide")
st.title("HubSpot CRM Migration Workbench")
st.caption("Preview · clean · validate · deduplicate — no HubSpot records are changed in this dashboard.")
uploaded = st.file_uploader("Upload a contacts CSV", type=["csv"])
if uploaded:
    frame = pd.read_csv(uploaded, dtype=str, keep_default_na=False)
    rows = frame.to_dict(orient="records")
else:
    sample_path = Path("sample_data/contacts.csv")
    rows = pd.read_csv(sample_path, dtype=str, keep_default_na=False).to_dict(orient="records")
    st.info("Showing safe sample data. Upload your own CSV to preview it locally.")
result = prepare_contacts(rows)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Source records", result["source_count"])
c2.metric("Ready to migrate", len(result["ready"]))
c3.metric("Duplicates", len(result["duplicates"]))
c4.metric("Rejected", len(result["rejected"]))
st.subheader("Migration preview")
st.dataframe(pd.DataFrame(result["ready"]), use_container_width=True, hide_index=True)
left, right = st.columns(2)
with left:
    st.subheader("Duplicate records")
    st.dataframe(pd.DataFrame(result["duplicates"]), use_container_width=True, hide_index=True)
with right:
    st.subheader("Validation issues")
    st.dataframe(pd.DataFrame(result["rejected"]), use_container_width=True, hide_index=True)
st.download_button("Download cleaned contacts CSV", pd.DataFrame(result["ready"]).to_csv(index=False), file_name="hubspot_contacts_preview.csv", mime="text/csv")
st.warning("Live writes are intentionally available only through the CLI, with an explicit confirmation flag and environment setting.")
