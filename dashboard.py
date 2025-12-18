import streamlit as st
import pandas as pd
from leadgen.loaders import load_leads
from leadgen.data_enrichment import enrich_lead
from leadgen.score_engine import compute_propensity_score
import io
import os

st.set_page_config(page_title="3D In-Vitro: High-Probability Lead Dashboard", layout="wide")

st.title(":dna: High-Probability Lead Dashboard for 3D In-Vitro Models")

# Load leads (mock for demo)
data_fp = os.path.join("lead_data", "mock_leads.json")
raw_leads = load_leads(data_fp)

# Enrich (cache for demo)
@st.cache_data(show_spinner=False)
def get_enriched_leads(leads):
    enriched = [enrich_lead(l) for l in leads]
    df = pd.DataFrame(enriched)
    df["propensity_score"] = df.apply(compute_propensity_score, axis=1)
    df = df.sort_values("propensity_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)
    return df

df = get_enriched_leads(raw_leads)

# --- Sidebar Controls ---
st.sidebar.header("Search & Filter")

search_txt = st.sidebar.text_input("Name, Title, Company, Location", "")
hub_only = st.sidebar.checkbox("Major Hubs Only", False)
min_score = st.sidebar.slider("Min. Probability Score", 0, 100, 0)

filtered = df.copy()
if search_txt:
    regex = search_txt.lower()
    filtered = filtered[
        filtered.apply(lambda row: regex in str(row).lower(), axis=1)
    ]
if hub_only:
    filtered = filtered[filtered['location_major_hub']]
if min_score > 0:
    filtered = filtered[filtered['propensity_score'] >= min_score]

# Split by location
explicit_remote = filtered[filtered['person_location'].str.lower().str.contains("remote")]
hq_match = filtered[~filtered.index.isin(explicit_remote.index)]

st.markdown("### :trophy: Top High-Probability Leads")

cols = [
    "rank", "propensity_score", "name", "title", "company",
    "person_location", "company_hq", "business_email", "linkedin",
    "recommended_action"
]

def recommended_action(row):
    if row["propensity_score"] > 80:
        return "Contact Now"
    elif row["propensity_score"] > 60:
        return "Warm Outreach"
    else:
        return "Nurture"
filtered = filtered.copy()
filtered["recommended_action"] = filtered.apply(recommended_action, axis=1)


def linkify(link):
    if link.startswith("http"):
        return f"[LinkedIn]({link})"
    return ""
filtered["linkedin"] = filtered["linkedin"].apply(linkify)

st.dataframe(filtered[cols].reset_index(drop=True), use_container_width=True, hide_index=True)

# --- Export ---
st.markdown("---")
buff = io.StringIO()
if st.button(":floppy_disk: Export to CSV"):
    filtered[cols].to_csv(buff, index=False)
    st.download_button(label="Download Results as CSV", data=buff.getvalue(), file_name="high_probability_leads.csv", mime="text/csv")

st.write("\n")
st.markdown(
    """<small>Demo: All data is simulated for functional showcase. See README for design/logic and how to adapt with APIs or real data sources.</small>""",
    unsafe_allow_html=True
)

