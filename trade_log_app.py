import streamlit as st
import pandas as pd
from datetime import datetime

# Title
st.set_page_config(page_title="📈 Trade Log Dashboard", layout="wide")
st.title("📘 Options Trade Log (In-Memory)")

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
