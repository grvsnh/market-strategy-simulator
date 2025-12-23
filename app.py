"""
app.py

Market Strategy Simulator dashboard.
Uses reusable indicators, metrics, and visual buy/sell markers.
"""

from datetime import date

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.data_loader import load_market_data
from utils.metrics import (
    calculate_returns,
    total_return,
    max_drawdown,
    sharpe_ratio,
)
from strategies.moving_average import moving_average_crossover
from strategies.rsi import apply_rsi


# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="Market Strategy Simulator", layout="wide")

st.title("📊 Market Strategy Simulator")
st.write(
    "An interactive dashboard to analyze market data and "
    "visualize algorithmic strategies (analysis only, no trading)."
)

st.divider()


# -------------------------------------------------
# Load symbols
# -------------------------------------------------
@st.cache_data
def load_symbols():
    return pd.read_csv("data/symbols.csv")


symbols_df = load_symbols()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.header("Configuration")

row = st.sidebar.selectbox(
    "Select Company / Index",
    options=symbols_df.index,
    format_func=lambda i: f"{symbols_df.loc[i,'name']} ({symbols_df.loc[i,'symbol']})",
)

ticker = str(symbols_df.loc[row, "symbol"])

start_date = st.sidebar.date_input("Start Date", date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2023, 1, 1))

strategies = st.sidebar.multiselect(
    "Select Strategies",
    ["Moving Average", "RSI"],
    default=["Moving Average"],
)

if "Moving Average" in strategies:
    short_window = st.sidebar.slider("Short MA", 5, 50, 20)
    long_window = st.sidebar.slider("Long MA", 20, 200, 50)

if "RSI" in strategies:
    rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)

run = st.sidebar.button("Run Simulation")

# -------------------------------------------------
# Main logic
# -------------------------------------------------
if run:
    try:
        df = load_market_data(ticker, start_date, end_date)

        if "Moving Average" in strategies:
            df = moving_average_crossover(df, short_window, long_window)

        if "RSI" in strategies:
            df = apply_rsi(df, rsi_period)

        st.success(f"Loaded data for {ticker}")

        # -----------------------------
        # Metrics
        # -----------------------------
        returns = calculate_returns(df["Close"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Return", f"{total_return(df['Close'])*100:.2f}%")
        col2.metric("Max Drawdown", f"{max_drawdown(df['Close'])*100:.2f}%")
        col3.metric("Sharpe Ratio", f"{sharpe_ratio(returns):.2f}")

        # -----------------------------
        # Visualization
        # -----------------------------
        rows = 2 if "RSI" in strategies else 1

        fig = make_subplots(
            rows=rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            subplot_titles=[
                "Price, Moving Averages & Trade Signals",
                "Relative Strength Index (RSI)",
            ][:rows],
        )

        # Price
        fig.add_trace(
            go.Scatter(x=df.index, y=df["Close"], name="Close"),
            row=1,
            col=1,
        )

        # Moving averages + Buy/Sell markers
        if "Moving Average" in strategies:
            fig.add_trace(
                go.Scatter(x=df.index, y=df["SMA_Short"], name="SMA Short"),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["SMA_Long"], name="SMA Long"),
                row=1,
                col=1,
            )

            buys = df[df["Position"] == 1]
            sells = df[df["Position"] == -1]

            fig.add_trace(
                go.Scatter(
                    x=buys.index,
                    y=buys["Close"],
                    mode="markers",
                    marker=dict(color="green", size=10, symbol="triangle-up"),
                    name="Buy",
                ),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=sells.index,
                    y=sells["Close"],
                    mode="markers",
                    marker=dict(color="red", size=10, symbol="triangle-down"),
                    name="Sell",
                ),
                row=1,
                col=1,
            )

        # RSI subplot
        if "RSI" in strategies:
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["RSI"], name="RSI", line=dict(color="orange")
                ),
                row=2,
                col=1,
            )

            fig.add_shape(
                type="line",
                x0=df.index.min(),
                x1=df.index.max(),
                y0=70,
                y1=70,
                line=dict(color="red", dash="dash"),
                row=2,
                col=1,
            )

            fig.add_shape(
                type="line",
                x0=df.index.min(),
                x1=df.index.max(),
                y0=30,
                y1=30,
                line=dict(color="green", dash="dash"),
                row=2,
                col=1,
            )

        fig.update_layout(height=750)
        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # Data preview
        # -----------------------------
        st.subheader("Data Preview")
        st.dataframe(df.tail(10), use_container_width=True)

    except Exception as e:
        st.error(str(e))
else:
    st.info("Configure settings and click **Run Simulation**.")
