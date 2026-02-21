import requests
import pandas as pd
from config import HF_TOKEN, SUMMARIZER_MODEL, CLASSIFIER_MODEL

API_BASE = "https://router.huggingface.co/hf-inference/models"
HEADERS  = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


# ── SAMPLE DATA ───────────────────────────────────────────────────────────────

def generate_sample_data():
    """
    Returns a sample campaign dataframe.
    In real use, replace this with pd.read_csv('your_file.csv')
    """
    data = {
        "campaign_name": [
            "Summer Awareness - Instagram",
            "Conversion Push - Google Ads",
            "Re-engagement - Email",
            "Brand Recall - YouTube",
            "Referral Drive - WhatsApp"
        ],
        "channel": ["Instagram", "Google Ads", "Email", "YouTube", "WhatsApp"],
        "type":    ["Awareness", "Conversion", "Retention", "Awareness", "Referral"],
        "impressions":       [120000, 85000, 40000, 200000, 30000],
        "clicks":            [4800,   6800,  2800,  5000,   1800],
        "conversions":       [96,     544,   196,   75,     270],
        "spend_inr":         [50000,  80000, 20000, 90000,  15000],
        "revenue_inr":       [192000, 544000,196000,150000, 270000],
        "content_description": [
            "Promoted brand awareness for mutual funds targeting young investors in metro cities.",
            "Ran conversion ads for SIP sign-ups targeting working professionals aged 25-35.",
            "Sent re-engagement emails to inactive users with personalised fund recommendations.",
            "YouTube pre-roll ads to improve brand recall among first-time investors.",
            "WhatsApp referral campaign asking existing users to invite friends for bonus rewards."
        ]
    }
    df = pd.DataFrame(data)
    df["ctr_pct"]              = (df["clicks"] / df["impressions"] * 100).round(2)
    df["conversion_rate_pct"]  = (df["conversions"] / df["clicks"] * 100).round(2)
    df["roas"]                 = (df["revenue_inr"] / df["spend_inr"]).round(2)
    return df


# ── KPI CALCULATIONS ──────────────────────────────────────────────────────────

def compute_kpis(df):
    """
    Takes the campaign dataframe and returns a dict of overall KPIs.
    """
    return {
        "total_spend":       df["spend_inr"].sum(),
        "total_revenue":     df["revenue_inr"].sum(),
        "overall_roas":      round(df["revenue_inr"].sum() / df["spend_inr"].sum(), 2),
        "total_impressions": df["impressions"].sum(),
        "total_conversions": df["conversions"].sum(),
        "avg_ctr":           round(df["ctr_pct"].mean(), 2),
        "best_channel":      df.loc[df["roas"].idxmax(), "channel"],
        "worst_channel":     df.loc[df["roas"].idxmin(), "channel"],
    }


def build_report_text(df, kpis):
    """
    Converts KPIs and channel data into a paragraph of text.
    This text is what gets sent to the BART summarizer.
    LLMs work with text, so we convert our numbers into readable sentences first.
    """
    channel_summary = df.groupby("channel").agg(
        avg_roas=("roas", "mean"),
        total_spend=("spend_inr", "sum"),
        total_conversions=("conversions", "sum")
    ).round(2).to_string()

    return f"""
    Marketing Campaign Performance Report:

    Total spend: INR {kpis['total_spend']:,}
    Total revenue: INR {kpis['total_revenue']:,}
    Overall ROAS: {kpis['overall_roas']}x
    Total impressions: {kpis['total_impressions']:,}
    Total conversions: {kpis['total_conversions']:,}
    Average CTR: {kpis['avg_ctr']}%
    Best performing channel: {kpis['best_channel']}
    Worst performing channel: {kpis['worst_channel']}

    Channel breakdown:
    {channel_summary}
    """


# ── HUGGINGFACE API CALLS ─────────────────────────────────────────────────────

def summarize(text):
    """
    Sends report text to BART summarization model.
    Returns a plain-English executive summary.
    """
    url     = f"{API_BASE}/{SUMMARIZER_MODEL}"
    payload = {
        "inputs": text[:1000],  # BART works best under 1024 tokens
        "parameters": {
            "max_length": 180,
            "min_length": 60,
            "do_sample": False
        }
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()[0]["summary_text"]
        elif response.status_code == 503:
            return "Model is loading. Wait 20 seconds and try again."
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"


