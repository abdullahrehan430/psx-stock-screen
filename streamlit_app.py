# psx_stock_screen.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PSX Stock Screener", layout="wide")

st.title("📈 PSX Stock Screener & Trading Assistant")
st.markdown("This tool helps you identify the **top 5 stocks** for day trading and value investing on PSX.")

# ---- Simulated PSX Data ----
np.random.seed(42)
tickers = ["HBL", "LUCK", "MCB", "TPLP", "SYS", "ENGRO", "EPCL", "UNITY", "SNGP", "JSCL"]
data = {
    "Ticker": tickers,
    "Price": np.random.randint(100, 1500, len(tickers)),
    "Volume": np.random.randint(100000, 1000000, len(tickers)),
    "RSI": np.random.uniform(20, 80, len(tickers)),
    "PE Ratio": np.random.uniform(4, 18, len(tickers)),
    "Dividend Yield": np.random.uniform(2, 10, len(tickers)),
    "EPS": np.random.uniform(5, 40, len(tickers))
}
df = pd.DataFrame(data)

# ---- Filters ----
st.sidebar.header("📊 Filter Options")

rsi_max = st.sidebar.slider("Max RSI (for oversold)", min_value=10, max_value=70, value=35)
min_volume = st.sidebar.number_input("Min Volume", value=300000)

# ---- Daily Trading Picks ----
st.subheader("🔥 Top 5 Daily Trading Stocks")

trading_df = df[
    (df["RSI"] <= rsi_max) &
    (df["Volume"] >= min_volume)
].sort_values(by=["Volume", "RSI"], ascending=[False, True]).head(5)

st.dataframe(trading_df)

# ---- Long-Term Value Picks ----
st.subheader("🏦 Top Value Investing Picks (Buffett Style)")

value_df = df[
    (df["PE Ratio"] < 12) &
    (df["Dividend Yield"] > 4)
].sort_values(by=["PE Ratio", "Dividend Yield"], ascending=[True, False]).head(5)

st.dataframe(value_df)

# ---- Visualization ----
st.subheader("📉 RSI Distribution of All Stocks")
st.bar_chart(df.set_index("Ticker")["RSI"])
