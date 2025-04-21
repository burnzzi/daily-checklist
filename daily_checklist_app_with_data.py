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

# Checklist
st.subheader("🧾 Pre-Trading Checklist")
checklist_items = [
    "Review overnight futures movement (NQ)",
    "Check premarket trend for TQQQ/SQQQ",
    "Analyze VIX level and trend",
    "Scan for news impacting QQQ/NQ",
    "Mark key support/resistance levels",
    "Identify opening range breakout potential",
    "Set alerts for key levels",
    "Define your entry/exit plan",
    "Verify position size and risk level"
]

for item in checklist_items:
    st.checkbox(item)
