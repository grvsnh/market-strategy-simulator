"""
symbols.py

Loads available market symbols for user selection.
"""

import pandas as pd


def load_symbols(path: str = "data/symbols.csv") -> pd.DataFrame:
    """
    Load available stock symbols from a CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: symbol, name
    """
    df = pd.read_csv(path)
    return df
