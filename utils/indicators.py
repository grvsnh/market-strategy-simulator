"""
indicators.py

Reusable technical indicator calculations.
No UI, no plotting, no strategy logic.
"""

import pandas as pd


def simple_moving_average(
    series: pd.Series,
    window: int,
) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA).

    Parameters
    ----------
    series : pd.Series
        Price series (e.g. Close)
    window : int
        Lookback window

    Returns
    -------
    pd.Series
        SMA series
    """
    return series.rolling(window=window).mean()


def relative_strength_index(
    series: pd.Series,
    period: int = 14,
) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).

    Parameters
    ----------
    series : pd.Series
        Price series (e.g. Close)
    period : int
        RSI lookback period

    Returns
    -------
    pd.Series
        RSI values
    """
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
