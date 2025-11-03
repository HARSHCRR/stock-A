# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Three Ways to Run the Analysis

### 1. Jupyter Notebook (Recommended for Learning)

```bash
jupyter notebook notebooks/stock_analysis.ipynb
```

This provides:
- Step-by-step explanation
- Interactive code cells
- Inline visualizations
- Full narrative

### 2. CLI Report (Fast & Automated)

```bash
# Basic usage
python cli_report.py AAPL MSFT GOOGL AMZN TSLA

# Custom date range
python cli_report.py AAPL MSFT --start 2020-01-01 --end 2023-12-31

# With risk-free rate
python cli_report.py AAPL MSFT --rf 0.02 --output my_reports/
```

Generates:
- CSV files with data and statistics
- PNG charts in output directory
- Console report

### 3. Streamlit Dashboard (Interactive)

```bash
streamlit run app.py
```

Features:
- Interactive ticker selection
- Date range picker
- Adjustable risk-free rate
- Real-time chart generation
- Download results

## Expected Outputs

After running any method, you'll have:

```
data/
├── raw_prices.csv          # Raw price data
├── clean_prices.csv        # Cleaned data
└── summary_stats.csv       # Calculated metrics

slides/ (or output directory)
├── equity_curves.png
├── performance_metrics.png
├── rolling_volatility.png
├── max_drawdown.png
└── sharpe_ratios.png
```

## Troubleshooting

**Issue**: `ModuleNotFoundError`
- **Solution**: Ensure you're in the project root directory when running scripts
- Make sure `src/` directory exists and has `__init__.py`

**Issue**: `yfinance` download fails
- **Solution**: Check internet connection and ticker symbols
- Some tickers may not have data for specified dates

**Issue**: Charts not displaying
- **Solution**: Install matplotlib and seaborn: `pip install matplotlib seaborn`

## Next Steps

1. Run the notebook to understand each step
2. Modify tickers or date ranges in the notebook
3. Explore the Streamlit dashboard for interactivity
4. Use CLI report for batch processing

