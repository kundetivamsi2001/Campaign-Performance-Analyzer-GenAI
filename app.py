import streamlit as st
import pandas as pd
from model import (
    generate_sample_data,
    compute_kpis,
    build_report_text,
    summarize,
    
)


def show_table(df):
    # Converts dataframe to plain HTML table — avoids pyarrow/numpy crash entirely
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Campaign Analyzer", layout="wide")
    st.title("Campaign Performance Analyzer")
    st.markdown("Analyzes campaign data and generates AI-powered insights using HuggingFace BART.")
    st.markdown("---")

    # ── SAMPLE CSV DOWNLOAD ───────────────────────────────────────────────────
    st.subheader("Step 1 — Load Campaign Data")
    st.markdown("Download the sample CSV below, fill it with your data, then upload it.")

    sample_df = generate_sample_data()
    csv_bytes = sample_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label     = "Download Sample CSV",
        data      = csv_bytes,
        file_name = "sample_campaigns.csv",
        mime      = "text/csv"
    )

    uploaded = st.file_uploader("Upload your campaign CSV", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df)} campaigns from your file.")
    else:
        df = generate_sample_data()
        st.info("No file uploaded. Showing sample data.")

    # ── KPI DASHBOARD ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Step 2 — Campaign KPIs")

    kpis = compute_kpis(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spend",       f"Rs.{kpis['total_spend']:,}")
    col2.metric("Total Revenue",     f"Rs.{kpis['total_revenue']:,}")
    col3.metric("Overall ROAS",      f"{kpis['overall_roas']}x")
    col4.metric("Total Conversions", f"{kpis['total_conversions']:,}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Avg CTR",       f"{kpis['avg_ctr']}%")
    col6.metric("Best Channel",  kpis["best_channel"])
    col7.metric("Worst Channel", kpis["worst_channel"])

    # ── RAW DATA TABLE ────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Campaign Data")

    show_cols = ["campaign_name", "channel", "type", "roas", "ctr_pct", "spend_inr", "revenue_inr"]
    available = [c for c in show_cols if c in df.columns]
    show_table(df[available].sort_values("roas", ascending=False).reset_index(drop=True))

    # ── AI SUMMARY ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Step 3 — AI Executive Summary")
    st.markdown("Uses **facebook/bart-large-cnn** to turn your campaign numbers into plain English.")

    if st.button("Generate AI Summary"):
        report_text = build_report_text(df, kpis)
        with st.spinner("Summarizing... (may take 20-30 seconds on first run)"):
            summary = summarize(report_text)
        st.success("Done!")
        st.write(summary)
        with st.expander("View raw text sent to model"):
            st.text(report_text)

   


if __name__ == "__main__":
    main()