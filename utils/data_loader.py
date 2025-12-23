"""
data_loader.py

Handles fetching and preparing historical market data
using free data sources (Yahoo Finance via yfinance).

This module contains NO UI or strategy logic.
"""

from datetime import date
import pandas as pd
import yfinance as yf
import streamlit as st


@st.cache_data(show_spinner=False)
def load_market_data(
    ticker: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """
    Fetch historical OHLCV market data for a given ticker.

    Parameters
    ----------
    ticker : str
        Stock or index symbol (e.g. 'AAPL', 'RELIANCE.NS', '^NSEI')
    start_date : date
        Start date for historical data
    end_date : date
        End date for historical data

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with OHLCV columns indexed by date

    Raises
    ------
    ValueError
        If ticker is empty or no data is returned
    """

    # -----------------------------
    # Input validation
    # -----------------------------
    if not ticker or not ticker.strip():
        raise ValueError("Ticker symbol cannot be empty")

    # -----------------------------
    # Download data
    # -----------------------------
    df = yf.download(
        ticker.strip().upper(),
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=False,
    )

    # -----------------------------
    # Defensive checks
    # -----------------------------
    if df is None or df.empty:
        raise ValueError(f"No data found for ticker '{ticker}'")

    # -----------------------------
    # FIX: Flatten MultiIndex columns from yfinance
    # -----------------------------
    # yfinance often returns columns like ('Close', 'AAPL')
    # Plotly and indicators require 1D Series
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # -----------------------------
    # Keep standard OHLCV columns only
    # -----------------------------
    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    df = df[required_columns]

    # -----------------------------
    # Final cleanup
    # -----------------------------
    df.dropna(inplace=True)
    df.index.name = "Date"

    return df
