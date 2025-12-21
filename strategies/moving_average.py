"""
moving_average.py

Implements a Moving Average (MA) crossover strategy.
Pure strategy logic only — no UI, no plotting.
"""

import pandas as pd


def moving_average_crossover(
    data: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    """
    Apply a moving average crossover strategy to market data.

    Parameters
    ----------
    data : pd.DataFrame
        Market data containing a 'Close' column
    short_window : int
        Window size for the short moving average
    long_window : int
        Window size for the long moving average

    Returns
    -------
    pd.DataFrame
        DataFrame with added columns:
        - SMA_Short
        - SMA_Long
        - Signal
        - Position
    """

    # --- Validation ---
    if "Close" not in data.columns:
        raise ValueError("Data must contain a 'Close' column")

    if short_window >= long_window:
        raise ValueError("Short window must be smaller than long window")

    df = data.copy()

    # --- Moving averages ---
    df["SMA_Short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_Long"] = df["Close"].rolling(window=long_window).mean()

    # --- Signal generation (vectorized & safe) ---
    df["Signal"] = 0
    df["Signal"] = (df["SMA_Short"] > df["SMA_Long"]).astype(int)

    # Remove early-period noise
    df.loc[: df.index[long_window - 1], "Signal"] = 0

    # --- Position changes ---
    df["Position"] = df["Signal"].diff()

    return df
