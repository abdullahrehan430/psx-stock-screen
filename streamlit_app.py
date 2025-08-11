# psx_stock_screen.py
import streamlit as st
import pandas as pd
import numpy as np
import websocket
import json
import threading
import time

st.set_page_config(page_title="PSX Stock Screener", layout="wide")
st.title("📈 PSX Stock Screener & Trading Assistant (Live Data)")

# ---- Global storage for live data ----
live_data = []

# ---- WebSocket Callbacks ----
def on_message(ws, message):
    global live_data
    try:
        data = json.loads(message)
        # Expecting dict with "symbol", "ltp" (last traded price), "volume"
        if isinstance(data, dict) and "symbol" in data:
            live_data.append({
                "Ticker": data.get("symbol"),
                "Price": data.get("ltp", 0),
                "Volume": data.get("volume", 0)
            })
    except:
        pass

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def run_websocket():
    ws = websocket.WebSocketApp(
        "wss://psxterminal.com/",  # Free real-time PSX feed
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

# Start WebSocket in background
threading.Thread(target=run_websocket, daemon=True).start()

# ---- Sidebar Filters ----
st.sidebar.header("📊 Filter Options")
rsi_max = st.sidebar.slider("Max RSI (for oversold)", min_value=10, max_value=70, value=35)
min_volume = st.sidebar.number_input("Min Volume", value=300000)

# ---- Main Loop ----
placeholder_trading = st.empty()
placeholder_value = st.empty()
placeholder_chart = st.empty()

while True:
    if live_data:
        # Create DataFrame from latest snapshot
        df = pd.DataFrame(live_data).drop_duplicates(subset="Ticker", keep="last")

        # Add simulated RSI, PE, Dividend, EPS (can replace with real calcs if data available)
        np.random.seed(42)
        df["RSI"] = np.random.uniform(20, 80, len(df))
        df["PE Ratio"] = np.random.uniform(4, 18, len(df))
        df["Dividend Yield"] = np.random.uniform(2, 10, len(df))
        df["EPS"] = np.random.uniform(5, 40, len(df))

        # ---- Daily Trading Picks ----
        trading_df = df[
            (df["RSI"] <= rsi_max) &
            (df["Volume"] >= min_volume)
        ].sort_values(by=["Volume", "RSI"], ascending=[False, True]).head(5)

        placeholder_trading.subheader("🔥 Top 5 Daily Trading Stocks")
        placeholder_trading.dataframe(trading_df)

        # ---- Long-Term Value Picks ----
        value_df = df[
            (df["PE Ratio"] < 12) &
            (df["Dividend Yield"] > 4)
        ].sort_values(by=["PE Ratio", "Dividend Yield"], ascending=[True, False]).head(5)

        placeholder_value.subheader("🏦 Top Value Investing Picks (Buffett Style)")
        placeholder_value.dataframe(value_df)

        # ---- RSI Chart ----
        placeholder_chart.subheader("📉 RSI Distribution of All Stocks")
        placeholder_chart.bar_chart(df.set_index("Ticker")["RSI"])

    time.sleep(3)
