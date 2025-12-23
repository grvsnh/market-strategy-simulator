# Utilities Module

This directory contains reusable utility components that support data loading, indicator calculation, and performance analysis for the **Market Strategy Simulator**.

These utilities are designed to be independent of the UI and strategy logic.

---

## 📁 Files

### `data_loader.py`

Handles fetching and preparing historical market data.

-   Retrieves OHLCV data from Yahoo Finance
-   Cleans and normalizes data formats
-   Implements caching for improved performance

---

### `symbols.py`

Manages symbol metadata used by the application.

-   Loads curated market symbols from CSV
-   Supports quick selection of popular stocks and indices
-   Acts as a convenience layer, not a limitation

---

### `indicators.py`

Provides reusable technical indicator calculations.

-   Simple Moving Average (SMA)
-   Relative Strength Index (RSI)
-   Designed for reuse across multiple strategies

---

### `metrics.py`

Implements performance evaluation metrics.

-   Total return
-   Maximum drawdown
-   Sharpe ratio
-   Used for analytical insight and comparison

---

## 🧠 Design Principles

-   Pure functions with no UI dependencies
-   Reusable across strategies
-   Clean separation of concerns
-   Easy to extend with additional utilities

---

## ⚠️ Disclaimer

Utilities in this directory are provided for **educational analysis only** and do not constitute financial or investment advice.
