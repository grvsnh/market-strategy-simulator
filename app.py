"""
app.py

Main entry point for the Market Strategy Simulator dashboard.
Provides an interactive UI to explore market data and simulate strategies.
"""

from datetime import date

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_market_data
from strategies.moving_average import moving_average_crossover


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Market Strategy Simulator",
    layout="wide",
)

st.title("📊 Market Strategy Simulator")
st.write(
    """
    An interactive dashboard to explore historical market data and
    simulate algorithmic trading strategies using free market data.
    """
)

st.divider()


# -------------------------------------------------------------------
# Load symbol list
# -------------------------------------------------------------------
@st.cache_data
def load_symbols():
    return pd.read_csv("data/symbols.csv")


symbols_df = load_symbols()

# -------------------------------------------------------------------
# Sidebar – User controls
# -------------------------------------------------------------------
st.sidebar.header("Configuration")

# Company selector (UX FIX)
selected_row = st.sidebar.selectbox(
    "Select Company / Index",
    options=symbols_df.index,
    format_func=lambda i: f"{symbols_df.loc[i, 'name']} ({symbols_df.loc[i, 'symbol']})",
)

ticker = str(symbols_df.loc[selected_row, "symbol"])

# Date inputs
start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2022, 1, 1),
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date(2023, 1, 1),
)

# Strategy parameters
st.sidebar.subheader("Moving Average Strategy")

short_window = st.sidebar.slider(
    "Short MA Window",
    min_value=5,
    max_value=50,
    value=20,
)

long_window = st.sidebar.slider(
    "Long MA Window",
    min_value=20,
    max_value=200,
    value=50,
)

run_button = st.sidebar.button("Run Simulation")

# -------------------------------------------------------------------
# Main logic
# -------------------------------------------------------------------
if run_button:
    try:
        # Load market data
        df = load_market_data(ticker, start_date, end_date)

        # Apply Moving Average strategy
        df_signals = moving_average_crossover(
            df,
            short_window=short_window,
            long_window=long_window,
        )

        st.success(f"Loaded data for {ticker}")

        # ------------------------------------------------------------
        # Data preview
        # ------------------------------------------------------------
        st.subheader("Market Data Preview")
        st.dataframe(df_signals.tail(10), use_container_width=True)

        # ------------------------------------------------------------
        # Visualization
        # ------------------------------------------------------------
        st.subheader("Price & Moving Averages")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df_signals.index,
                y=df_signals["Close"],
                name="Close Price",
                line=dict(width=1),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df_signals.index,
                y=df_signals["SMA_Short"],
                name=f"SMA {short_window}",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df_signals.index,
                y=df_signals["SMA_Long"],
                name=f"SMA {long_window}",
            )
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price",
            legend_title="Legend",
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(str(e))

else:
    st.info("Select a company, adjust parameters, and click **Run Simulation**.")
