"""
symbols.py

Utility for loading and managing market symbols.
"""

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_symbols(path: str = "data/symbols.csv") -> pd.DataFrame:
    """
    Load available market symbols from CSV.

    Parameters
    ----------
    path : str
        Path to symbols CSV file

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: symbol, name
    """
    df = pd.read_csv(path)

    if not {"symbol", "name"}.issubset(df.columns):
        raise ValueError("symbols.csv must contain 'symbol' and 'name' columns")

    return df
