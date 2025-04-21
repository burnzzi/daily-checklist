
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="TQQQ/SQQQ Dashboard", layout="wide")

# Title and date
st.title("📈 TQQQ / SQQQ Daily Trading Checklist + Live Data")
st.subheader(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}")

# --- LIVE DATA SECTION ---
st.markdown("## 🔴 Live Data Snapshot (Coming Soon)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("TQQQ Price", "Loading...", delta="...")
    st.metric("SQQQ Price", "Loading...", delta="...")

with col2:
    st.metric("VIX", "Loading...", delta="...")

with col3:
    st.metric("Nasdaq Futures (NQ)", "Loading...", delta="...")

st.info("Live data connections will be added next using Yahoo Finance API or another free source.")

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
