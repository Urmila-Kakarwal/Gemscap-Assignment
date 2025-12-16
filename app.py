import streamlit as st
import requests
import pandas as pd
import numpy as np
import altair as alt
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Quant Trading Dashboard", layout="wide")
st.title("📊 Real-Time Quant Trading Analytics Dashboard")

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("Controls")
window = st.sidebar.slider("Z-Score Window", 10, 100, 30)
z_threshold = st.sidebar.slider("Z-Score Alert Threshold", 1.0, 3.0, 2.0)

st.sidebar.divider()
st.sidebar.subheader("📥 Export Data")

# ---------------- SESSION STATE ----------------
for key in ["btc", "eth", "spread", "zscore"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=1000, key="refresh")

# ---------------- FUNCTIONS ----------------
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url, timeout=5).json()["price"])

def compute_zscore(series, window):
    if len(series) < window:
        return None
    arr = np.array(series[-window:])
    std = arr.std()
    if std == 0:
        return 0.0
    return (arr[-1] - arr.mean()) / std

# ---------------- FETCH DATA ----------------
btc_price = get_price("BTCUSDT")
eth_price = get_price("ETHUSDT")

st.session_state.btc.append(btc_price)
st.session_state.eth.append(eth_price)

spread = btc_price - eth_price
st.session_state.spread.append(spread)

z = compute_zscore(st.session_state.spread, window)
st.session_state.zscore.append(z)

# ---------------- DATAFRAME ----------------
df = pd.DataFrame({
    "Time": range(len(st.session_state.btc)),
    "BTC": st.session_state.btc,
    "ETH": st.session_state.eth,
    "Spread": st.session_state.spread,
    "ZScore": st.session_state.zscore
})

# ---------------- SIDEBAR DOWNLOAD ----------------
st.sidebar.download_button(
    "⬇ Download CSV",
    data=df.to_csv(index=False),
    file_name="quant_dashboard_data.csv",
    mime="text/csv",
    key="download_csv"
)

# ---------------- METRICS ----------------
col1, col2 = st.columns(2)
col1.metric("BTCUSDT Price", round(btc_price, 2))
col2.metric("ETHUSDT Price", round(eth_price, 2))

st.divider()

# ---------------- PRICE CHARTS ----------------
col1, col2 = st.columns(2)

btc_chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x="Time",
    y="BTC"
).properties(height=250)

eth_chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x="Time",
    y="ETH"
).properties(height=250)

col1.altair_chart(btc_chart, use_container_width=True)
col2.altair_chart(eth_chart, use_container_width=True)

st.divider()

# ---------------- SPREAD CHART ----------------
st.subheader("Spread (BTC − ETH)")

spread_chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
    x="Time",
    y="Spread"
).properties(height=260)

st.altair_chart(spread_chart, use_container_width=True)

# ---------------- Z-SCORE CHART WITH ALERTS ----------------
st.subheader("Z-Score (Alerts Marked in Red)")

z_df = df.dropna(subset=["ZScore"]).copy()

if not z_df.empty:
    z_df["Alert"] = abs(z_df["ZScore"]) > z_threshold

    z_line = alt.Chart(z_df).mark_line(strokeWidth=2).encode(
        x="Time",
        y="ZScore"
    )

    alert_points = alt.Chart(z_df[z_df["Alert"]]).mark_point(
        size=80,
        color="red"
    ).encode(
        x="Time",
        y="ZScore"
    )

    st.altair_chart(z_line + alert_points, use_container_width=True)

    latest_z = z_df["ZScore"].iloc[-1]
    if abs(latest_z) > z_threshold:
        st.error(f" Z-Score Alert: {latest_z:.2f}")
    else:
        st.success(f"Z-Score Normal: {latest_z:.2f}")

else:
    st.info("Waiting for enough data to compute Z-Score...")

st.caption("Z-Score appears after rolling window is filled • Charts rendered with Altair (SVG)")