"""
moving_average.py

Moving Average crossover strategy.
Uses shared indicators from utils.indicators.
"""

import pandas as pd
from utils.indicators import simple_moving_average


def moving_average_crossover(
    data: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    if "Close" not in data.columns:
        raise ValueError("Data must contain a 'Close' column")

    if short_window >= long_window:
        raise ValueError("Short window must be smaller than long window")

    df = data.copy()

    df["SMA_Short"] = simple_moving_average(df["Close"], short_window)
    df["SMA_Long"] = simple_moving_average(df["Close"], long_window)

    # Signal: 1 = bullish, 0 = bearish
    df["Signal"] = (df["SMA_Short"] > df["SMA_Long"]).astype(int)

    # Position change: +1 = Buy, -1 = Sell
    df["Position"] = df["Signal"].diff()

    return df
