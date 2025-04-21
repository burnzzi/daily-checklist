import streamlit as st
import yfinance as yf
import finnhub
import os

# Load Finnhub API key from Streamlit Secrets
api_key = st.secrets.get("FINNHUB_API_KEY", None)
if api_key is None:
    st.error("⚠️ Finnhub API key is missing in your Streamlit secrets.")
    st.stop()

# Setup Finnhub client
finnhub_client = finnhub.Client(api_key=api_key)

# Finnhub fetch for VIX and Nasdaq Futures (NQ)
def get_vix_nq_finnhub():
    try:
        vix_data = finnhub_client.quote("^VIX")
        nq_data = finnhub_client.quote("NQ=F")
        vix_price = vix_data["c"]
        nq_price = nq_data["c"]
    except Exception as e:
        vix_price, nq_price = float("nan"), float("nan")
    return vix_price, nq_price

# yFinance fetch for TQQQ and SQQQ
def get_live_data():
    try:
        tqqq = yf.download("TQQQ", period="1d", interval="1m")
        sqqq = yf.download("SQQQ", period="1d", interval="1m")

        tqqq_price = tqqq["Close"].dropna().iloc[-1] if not tqqq.empty else float("nan")
        sqqq_price = sqqq["Close"].dropna().iloc[-1] if not sqqq.empty else float("nan")
    except:
        tqqq_price, sqqq_price = float("nan"), float("nan")

    vix_price, nq_price = get_vix_nq_finnhub()
    return tqqq_price, sqqq_price, vix_price, nq_price

# Streamlit layout
st.set_page_config(page_title="TQQQ/SQQQ Daily Checklist", layout="wide")
st.title("📊 TQQQ/SQQQ Daily Trading Checklist")

# Get and display data
tqqq_price, sqqq_price, vix_price, nq_price = get_live_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("TQQQ", f"${tqqq_price:.2f}" if tqqq_price == tqqq_price else "N/A")
col2.metric("SQQQ", f"${sqqq_price:.2f}" if sqqq_price == sqqq_price else "N/A")
col3.metric("VIX", f"{vix_price:.2f}" if vix_price == vix_price else "N/A")
col4.metric("Nasdaq Futures (NQ)", f"${nq_price:.2f}" if nq_price == nq_price else "N/A")

# Daily checklist
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
