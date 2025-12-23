# Data Directory

This directory contains datasets used by the **Market Strategy Simulator** project.

The project is intentionally designed to **not store large historical market data locally**.
Instead, it fetches market data dynamically from free public sources at runtime.

---

## 📄 Files in this Directory

### `symbols.csv`

A curated list of commonly used market symbols for quick selection in the UI.

**Columns:**

-   `symbol` — Yahoo Finance–compatible ticker symbol
-   `name` — Human-readable company or index name

**Purpose:**

-   Improves usability by allowing users to select popular stocks and indices
-   Avoids requiring users to memorize ticker symbols
-   Acts as a convenience layer, not a limitation

The application also supports **manual ticker input**, allowing users to analyze
any Yahoo Finance–compatible asset beyond this list.

---

## 📊 Market Data Source

Historical market data (OHLCV) is fetched dynamically using:

-   **Yahoo Finance** via the `yfinance` Python library

This ensures:

-   Free and publicly accessible data
-   No API keys required
-   Up-to-date historical pricing
-   No large datasets stored in the repository

---

## ⚠️ Why Market Data Is Not Stored Here

Storing full historical price data locally would:

-   Increase repository size unnecessarily
-   Require frequent updates
-   Reduce flexibility

Instead, data is retrieved on demand and cached temporarily during runtime for performance.

---

## 🎓 Academic Integrity Note (CS50)

This project:

-   Uses only free, publicly available data
-   Performs **analysis and visualization only**
-   Does **not** execute or recommend real trades

The focus is on **learning algorithmic strategy concepts**, not financial advice.
