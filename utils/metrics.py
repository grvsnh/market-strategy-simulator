"""
metrics.py

Performance metrics for strategy analysis.
This module evaluates results; it does NOT execute trades.
"""

import pandas as pd
import numpy as np


def calculate_returns(
    series: pd.Series,
) -> pd.Series:
    """
    Calculate daily percentage returns.

    Parameters
    ----------
    series : pd.Series
        Price or portfolio value series

    Returns
    -------
    pd.Series
        Daily returns
    """
    return series.pct_change().dropna()


def total_return(
    series: pd.Series,
) -> float:
    """
    Calculate total return over the period.

    Returns
    -------
    float
        Total return (e.g. 0.25 = 25%)
    """
    return (series.iloc[-1] / series.iloc[0]) - 1


def max_drawdown(
    series: pd.Series,
) -> float:
    """
    Calculate maximum drawdown.

    Returns
    -------
    float
        Maximum drawdown (negative value)
    """
    rolling_max = series.cummax()
    drawdown = (series - rolling_max) / rolling_max
    return drawdown.min()


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = 252,
) -> float:
    """
    Calculate annualized Sharpe Ratio.

    Parameters
    ----------
    returns : pd.Series
        Daily returns
    risk_free_rate : float
        Annual risk-free rate
    trading_days : int
        Trading days per year

    Returns
    -------
    float
        Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / trading_days)

    if excess_returns.std() == 0:
        return 0.0

    return np.sqrt(trading_days) * (excess_returns.mean() / excess_returns.std())
