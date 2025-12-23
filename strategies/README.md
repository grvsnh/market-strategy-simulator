# Strategies Module

This directory contains implementations of algorithmic trading strategies used by the **Market Strategy Simulator**.

Each strategy focuses on **signal generation and analysis**, not real trade execution.

---

## 📁 Files

### `moving_average.py`

Implements a **Moving Average (MA) crossover strategy**.

-   Calculates short-term and long-term simple moving averages
-   Generates bullish and bearish signals based on crossovers
-   Identifies buy and sell points for visualization purposes

---

### `rsi.py`

Implements the **Relative Strength Index (RSI)** indicator.

-   Calculates RSI values for a given lookback period
-   Helps identify overbought and oversold conditions
-   Used for visualization and analytical insight only

---

## 🧠 Design Principles

-   Each strategy is isolated and reusable
-   No UI or plotting logic is included
-   No real trades are executed
-   Strategies operate on clean market data provided by utility modules

---

## ⚠️ Disclaimer

Strategies implemented in this directory are intended **for educational and analytical purposes only** and should not be considered financial advice.
