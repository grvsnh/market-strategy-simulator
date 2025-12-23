"""
rsi.py

RSI indicator strategy wrapper.
Uses shared indicators from utils.indicators.
"""

import pandas as pd
from utils.indicators import relative_strength_index


def apply_rsi(
    data: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    if "Close" not in data.columns:
        raise ValueError("Data must contain a 'Close' column")

    df = data.copy()
    df["RSI"] = relative_strength_index(df["Close"], period)

    return df
