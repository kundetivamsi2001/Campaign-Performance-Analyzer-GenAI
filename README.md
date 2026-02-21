# Campaign Performance Analyzer using GenAI & LLMs

A Streamlit web app that ingests marketing campaign CSV data and uses
facebook/bart-large-cnn to automatically generate plain-English executive
summaries — replacing what previously required hours of manual reporting.

---

## What This Project Does

Campaign managers have raw CSV data with impressions, clicks, spend, and
revenue but no quick way to extract a clear story from it. This tool does two things:

**1. KPI Dashboard** — Automatically computes and displays Total Spend, Revenue,
ROAS, CTR, Conversions, and best and worst performing channels from your CSV.

**2. AI Executive Summary** — Converts all campaign metrics into a report and
passes it to BART to generate a plain-English paragraph that a non-technical
stakeholder can read immediately.

---

## Project Structure
```
campaign-analyzer/
│
├── app.py              # Streamlit UI — all frontend code lives here
├── model.py            # Core logic — API calls, KPI calculations, data processing
├── config.py           # HuggingFace token and model name (not pushed to GitHub)
├── requirements.txt    # Python dependencies
├── .gitignore          # Tells Git to ignore config.py and cache files
└── README.md           # This file
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI framework |
| HuggingFace Inference API | Runs the model without needing a local GPU |
| facebook/bart-large-cnn | Summarizes campaign report into plain English |
| Pandas | Data processing and KPI calculations |
| requests | HTTP calls to the HuggingFace API |

---

## Model Used

**facebook/bart-large-cnn**
A summarization model trained on news articles. Given a block of text describing
campaign performance numbers, it produces a concise summary. Used here to turn
raw metric data into an executive-friendly paragraph automatically.

---

## Sample CSV Files

Three ready-to-use sample datasets are included. Download any one and upload
it directly into the app.

**fintech_campaigns.csv**
8 campaigns modelled on a fintech investment app like Groww. Includes SIP
awareness, stock market sign-up conversion, tax saving ads, and referral
campaigns across Instagram, Google Ads, Email, YouTube, WhatsApp, and Facebook.

**ecommerce_campaigns.csv**
8 campaigns modelled on an online shopping platform. Includes Diwali sale
launch, electronics deals, cart abandonment recovery, flash sale, and app
install campaigns across multiple channels.

**food_beverage_campaigns.csv**
8 campaigns modelled on a food delivery platform like Swiggy. Includes city
launch awareness, midnight delivery offers, lapsed user win-back, weekend
combo deals, and subscription plan push campaigns.

All three files have the same 12 columns so any of them works with the app
without any changes.

**Required columns in your CSV:**
```
campaign_name, channel, type, impressions, clicks, conversions,
spend_inr, revenue_inr, content_description, ctr_pct, conversion_rate_pct, roas
```

If you are building your own CSV, make sure all 12 columns are present.
The app will throw a KeyError if any column is missing.

---

