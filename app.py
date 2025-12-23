"""
app.py

Market Strategy Simulator dashboard.
UI-polished version with improved layout and clarity.
"""

from datetime import date

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.data_loader import load_market_data
from utils.symbols import load_symbols
from utils.metrics import (
    calculate_returns,
    total_return,
    max_drawdown,
    sharpe_ratio,
)
from strategies.moving_average import moving_average_crossover
from strategies.rsi import apply_rsi


# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Market Strategy Simulator",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Market Strategy Simulator")
st.caption(
    "Analyze historical market data and visualize algorithmic strategies "
    "using free, public datasets (no live trading)."
)

st.divider()

# -------------------------------------------------
# Sidebar – Symbol Selection
# -------------------------------------------------
st.sidebar.header("🔍 Symbol Selection")

symbol_mode = st.sidebar.radio(
    "Choose selection method",
    ["Search Any Ticker", "Select from Popular List"],
)

ticker = None

if symbol_mode == "Search Any Ticker":
    ticker = (
        st.sidebar.text_input(
            "Enter Ticker Symbol",
            value="AAPL",
            help="Examples: AAPL, MSFT, RELIANCE.NS, ^NSEI, BTC-USD",
        )
        .strip()
        .upper()
    )
else:
    symbols_df = load_symbols()

    row = st.sidebar.selectbox(
        "Popular Symbols",
        options=symbols_df.index,
        format_func=lambda i: f"{symbols_df.loc[i,'name']} ({symbols_df.loc[i,'symbol']})",
    )

    ticker = str(symbols_df.loc[row, "symbol"])

# -------------------------------------------------
# Sidebar – Configuration
# -------------------------------------------------
st.sidebar.header("⚙️ Configuration")

start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2022, 1, 1),
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date(2023, 1, 1),
)

# Strategy selection
st.sidebar.header("📐 Strategies")

strategies = st.sidebar.multiselect(
    "Enable Strategies",
    ["Moving Average", "RSI"],
    default=["Moving Average"],
)

# Moving Average settings
if "Moving Average" in strategies:
    st.sidebar.subheader("Moving Average Settings")
    short_window = st.sidebar.slider("Short MA Window", 5, 50, 20)
    long_window = st.sidebar.slider("Long MA Window", 20, 200, 50)

# RSI settings
if "RSI" in strategies:
    st.sidebar.subheader("RSI Settings")
    rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)

run_button = st.sidebar.button("▶ Run Analysis", use_container_width=True)

# -------------------------------------------------
# Main logic
# -------------------------------------------------
if run_button:
    try:
        if not ticker:
            st.warning("Please enter or select a valid ticker symbol.")
            st.stop()

        df = load_market_data(ticker, start_date, end_date)

        if "Moving Average" in strategies:
            df = moving_average_crossover(df, short_window, long_window)

        if "RSI" in strategies:
            df = apply_rsi(df, rsi_period)

        st.success(f"Data loaded successfully for **{ticker}**")

        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------
        returns = calculate_returns(df["Close"])

        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Total Return", f"{total_return(df['Close']) * 100:.2f}%")
        col2.metric("📉 Max Drawdown", f"{max_drawdown(df['Close']) * 100:.2f}%")
        col3.metric("⚖️ Sharpe Ratio", f"{sharpe_ratio(returns):.2f}")

        st.divider()

        # -------------------------------------------------
        # Visualization
        # -------------------------------------------------
        rows = 2 if "RSI" in strategies else 1

        fig = make_subplots(
            rows=rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            subplot_titles=[
                "Price, Moving Averages & Buy/Sell Signals",
                "Relative Strength Index (RSI)",
            ][:rows],
        )

        # Price
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                name="Close Price",
                line=dict(width=2),
            ),
            row=1,
            col=1,
        )

        # Moving averages + Buy/Sell markers
        if "Moving Average" in strategies:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA_Short"],
                    name=f"SMA {short_window}",
                    line=dict(width=1.5),
                ),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA_Long"],
                    name=f"SMA {long_window}",
                    line=dict(width=1.5),
                ),
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
                    marker=dict(color="green", size=12, symbol="triangle-up"),
                    name="Buy Signal",
                ),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=sells.index,
                    y=sells["Close"],
                    mode="markers",
                    marker=dict(color="red", size=12, symbol="triangle-down"),
                    name="Sell Signal",
                ),
                row=1,
                col=1,
            )

        # RSI subplot
        if "RSI" in strategies:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["RSI"],
                    name="RSI",
                    line=dict(color="orange", width=2),
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

        fig.update_layout(
            height=800,
            legend_title="Indicators",
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # Data preview
        # -------------------------------------------------
        with st.expander("🔎 View Raw Data"):
            st.dataframe(df.tail(20), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info(
        "👈 Select a symbol, configure strategies, and click **Run Analysis** "
        "to visualize market behavior."
    )
