import streamlit as st
import yfinance as yf
import finnhub
from math import isnan  # <-- Add this at the top

# Load API key
api_key = st.secrets.get("FINNHUB_API_KEY", None)
if not api_key:
    st.error("⚠️ Finnhub API key is missing in your Streamlit secrets.")
    st.stop()

finnhub_client = finnhub.Client(api_key=api_key)

# Finnhub fetch for VIX and NQ
def get_vix_nq_finnhub():
    try:
        vix_data = finnhub_client.quote("^VIX")
        nq_data = finnhub_client.quote("NQ=F")
        vix_price = float(vix_data.get("c", float("nan")))
        nq_price = float(nq_data.get("c", float("nan")))
    except Exception:
        vix_price, nq_price = float("nan"), float("nan")
    return vix_price, nq_price

# yFinance fetch for TQQQ and SQQQ
def get_live_data():
    try:
        tqqq_df = yf.download("TQQQ", period="1d", interval="1m")
        sqqq_df = yf.download("SQQQ", period="1d", interval="1m")

        tqqq_price = float(tqqq_df["Close"].dropna().iloc[-1]) if not tqqq_df.empty else float("nan")
        sqqq_price = float(sqqq_df["Close"].dropna().iloc[-1]) if not sqqq_df.empty else float("nan")
    except:
        tqqq_price, sqqq_price = float("nan"), float("nan")

    vix_price, nq_price = get_vix_nq_finnhub()
    return tqqq_price, sqqq_price, vix_price, nq_price

# UI
st.set_page_config(page_title="TQQQ/SQQQ Daily Checklist", layout="wide")
st.title("📊 Daily Trading Checklist")

# Fetch prices
tqqq_price, sqqq_price, vix_price, nq_price = get_live_data()

# Display metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("TQQQ", f"${tqqq_price:.2f}" if not isnan(tqqq_price) else "N/A")
col2.metric("SQQQ", f"${sqqq_price:.2f}" if not isnan(sqqq_price) else "N/A")
col3.metric("VIX", f"{vix_price:.2f}" if not isnan(vix_price) else "N/A")
col4.metric("Nasdaq Futures (NQ)", f"${nq_price:.2f}" if not isnan(nq_price) else "N/A")

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
