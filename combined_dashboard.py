import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from math import isnan

# Title and page config
st.set_page_config(page_title="📈 Options Trading Dashboard", layout="wide")
st.title("📈 Trading Dashboard")

# Tabs for navigation
tab1, tab2 = st.tabs(["📝 Daily Checklist", "📘 Trade Log"])

# --- Tab 1: Daily Checklist ---
with tab1:
    # Live data for TQQQ, SQQQ, VIX, and Nasdaq Futures
    try:
        tqqq_data = yf.Ticker("TQQQ")
        tqqq_price = tqqq_data.history(period="1d")["Close"].iloc[-1]

        sqqq_data = yf.Ticker("SQQQ")
        sqqq_price = sqqq_data.history(period="1d")["Close"].iloc[-1]

        vix_data = yf.Ticker("^VIX")
        vix_price = vix_data.history(period="1d")["Close"].iloc[-1]

        nasdaq_futures_data = yf.Ticker("NQ=F")
        nasdaq_futures_price = nasdaq_futures_data.history(period="1d")["Close"].iloc[-1]
    except:
        tqqq_price = sqqq_price = vix_price = nasdaq_futures_price = "N/A"
    
    # Display live data in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TQQQ", f"${tqqq_price:.2f}" if not isnan(tqqq_price) else "N/A")
    col2.metric("SQQQ", f"${sqqq_price:.2f}" if not isnan(sqqq_price) else "N/A")
    col3.metric("VIX", f"{vix_price}" if not isnan(vix_price) else "N/A")
    col4.metric("Nasdaq Futures", f"${nasdaq_futures_price}" if not isnan(nasdaq_futures_price) else "N/A")
    
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

# --- Tab 2: Trade Log ---
with tab2:
    # Initialize session state for trade log
    if "trades" not in st.session_state:
        st.session_state.trades = []

    # Trade input form
    with st.form("trade_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Trade Date", datetime.today())
            ticker = st.selectbox("Ticker", ["TQQQ", "SQQQ", "Other"])
            direction = st.selectbox("Direction", ["Call", "Put"])
        with col2:
            entry = st.number_input("Entry Price", format="%.2f")
            exit = st.number_input("Exit Price", format="%.2f")
            contracts = st.number_input("Contracts", min_value=1, step=1)
        with col3:
            notes = st.text_input("Notes (optional)")
            submit = st.form_submit_button("Add Trade")

        if submit:
            return_pct = ((exit - entry) / entry) * 100 if direction == "Call" else ((entry - exit) / entry) * 100
            trade = {
                "Date": date.strftime("%Y-%m-%d"),
                "Ticker": ticker,
                "Direction": direction,
                "Entry": entry,
                "Exit": exit,
                "Contracts": contracts,
                "Return %": round(return_pct, 2),
                "Notes": notes
            }
            st.session_state.trades.append(trade)
            st.success("Trade added!")

    # Display trade table
    if st.session_state.trades:
        df = pd.DataFrame(st.session_state.trades)

        st.subheader("📋 Trade Log")
        st.dataframe(df, use_container_width=True)

        # Summary stats
        st.subheader("📊 Summary Stats")
        total_trades = len(df)
        winners = df[df["Return %"] > 0]
        win_rate = (len(winners) / total_trades) * 100 if total_trades > 0 else 0
        avg_return = df["Return %"].mean()
        total_return = df["Return %"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Trades", total_trades)
        col2.metric("Win Rate", f"{win_rate:.2f}%")
        col3.metric("Avg Return %", f"{avg_return:.2f}%")
        col4.metric("Cumulative Return", f"{total_return:.2f}%")

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Trade Log as CSV", csv, "trade_log.csv", "text/csv")
    else:
        st.info("No trades logged yet.")
