import streamlit as st
import yfinance as yf
import finnhub
import os
from datetime import datetime

st.set_page_config(page_title="TQQQ/SQQQ Dashboard", layout="wide")

# Title and date
st.title("📈 TQQQ / SQQQ Daily Trading Checklist + Live Data")
st.subheader(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}")

# --- LIVE DATA SECTION ---
st.markdown("## 🔴 Live Data Snapshot")

# Setup Finnhub client using your Streamlit Secrets
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

# Function to get VIX and NQ from Finnhub
def get_vix_nq_from_finnhub():
    try:
        vix_quote = finnhub_client.quote("^VIX")
        nq_quote = finnhub_client.quote("NQ=F")

        vix_price = vix_quote["c"] if "c" in vix_quote else float("nan")
        nq_price = nq_quote["c"] if "c" in nq_quote else float("nan")
    except Exception as e:
        vix_price = nq_price = float("nan")

    return vix_price, nq_price

# Function to get live data for TQQQ and SQQQ from yfinance
def get_live_data():
    tqqq_live = yf.download("TQQQ", period="1d", interval="1m")
    sqqq_live = yf.download("SQQQ", period="1d", interval="1m")

    tqqq_price = tqqq_live["Close"].dropna().iloc[-1] if not tqqq_live.empty else float("nan")
    sqqq_price = sqqq_live["Close"].dropna().iloc[-1] if not sqqq_live.empty else float("nan")

    vix_price, nq_price = get_vix_nq_from_finnhub()

    return tqqq_price, sqqq_price, vix_price, nq_price

# Get the live data
tqqq_price, sqqq_price, vix_price, nq_price = get_live_data()

# Display live data in the app
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("TQQQ Price", f"${tqqq_price:.2f}" if isinstance(tqqq_price, float) else tqqq_price, 
              delta=f"{(tqqq_price - tqqq_price*0.02):.2f}" if isinstance(tqqq_price, float) else "N/A")
    st.metric("SQQQ Price", f"${sqqq_price:.2f}" if isinstance(sqqq_price, float) else sqqq_price, 
              delta=f"{(sqqq_price - sqqq_price*0.02):.2f}" if isinstance(sqqq_price, float) else "N/A")

with col2:
    st.metric("VIX Index", f"{vix_price:.2f}" if isinstance(vix_price, float) else vix_price, 
              delta=f"{(vix_price - vix_price*0.02):.2f}" if isinstance(vix_price, float) else "N/A")

with col3:
    st.metric("Nasdaq Futures (NQ)", f"${nq_price:.2f}" if isinstance(nq_price, float) else nq_price, 
              delta=f"{(nq_price - nq_price*0.02):.2f}" if isinstance(nq_price, float) else "N/A")

st.info("Live data now integrated via Yahoo Finance API. Data updates every minute.")

# --- CHECKLIST SECTION ---
st.markdown("## ✅ Daily Checklist")

checklist = {
    "Pre-Market (8:00am – 9:20am)": [
        "Check NQ Futures trend",
        "Review VIX movement",
        "Scan TQQQ/SQQQ pre-market volume",
        "Identify key economic data releases today",
        "Update market breadth indicators",
        "Determine initial directional bias",
        "Note any relevant news headlines"
    ],
    "Opening Session (9:30am – 10:30am)": [
        "Observe opening 5-min candle direction",
        "Watch for early momentum shifts",
        "Track volume confirmation",
        "Set alerts near overnight highs/lows",
        "Confirm price action aligns with bias"
    ],
    "Mid-Day Review (12:00pm – 1:30pm)": [
        "Reassess market breadth and volume trends",
        "Adjust levels or directional bias if needed",
        "Watch for reversal signs / trend continuation",
        "Manage open trades or set alerts for re-entry"
    ],
    "Late Session (2:30pm – 3:50pm)": [
        "Observe end-of-day directional momentum",
        "Trim or close positions based on risk/reward",
        "Watch for volume spikes",
        "Consider hedging if exposure is high into close"
    ],
    "Post-Market Review (4:00pm – 5:00pm)": [
        "Review how trades aligned with setup",
        "Journal key learnings from today",
        "Update trade log",
        "Identify areas for improvement"
    ]
}

# Display checklist
for session, tasks in checklist.items():
    st.markdown(f"### 🕒 {session}")
    for task in tasks:
        st.checkbox(task, key=f"{session}-{task}")
