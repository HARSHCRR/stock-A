#!/usr/bin/env python3
"""
Simple example demonstrating the stock analysis pipeline.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import fetch_prices
from indicators import prepare_prices
from analysis import compute_daily_returns, annual_metrics, compute_cumulative_returns

def main():
    print("Stock Analysis Example")
    print("=" * 60)
    
    # Define stocks to analyze
    tickers = ['AAPL', 'MSFT']
    start_date = '2022-01-01'
    
    print(f"\n1. Fetching data for {', '.join(tickers)}...")
    prices = fetch_prices(tickers, start=start_date)
    print(f"   Fetched {len(prices)} days of data")
    
    print("\n2. Cleaning data...")
    prices_clean = prepare_prices(prices)
    print(f"   Clean data: {prices_clean.shape}")
    
    print("\n3. Computing returns...")
    daily_returns = compute_daily_returns(prices_clean)
    cum_returns = compute_cumulative_returns(daily_returns)
    print(f"   Daily returns: {daily_returns.shape}")
    
    print("\n4. Computing annualized metrics...")
    stats = annual_metrics(daily_returns, rf=0.0)
    print("\n   Summary Statistics:")
    print(stats.round(4))
    
    print("\n5. Final cumulative returns:")
    print(cum_returns.iloc[-1].round(4))
    
    print("\n" + "=" * 60)
    print("Example complete! Check the output above.")
    print("\nFor full analysis, run:")
    print("  - Jupyter notebook: jupyter notebook notebooks/stock_analysis.ipynb")
    print("  - CLI report: python cli_report.py AAPL MSFT GOOGL")
    print("  - Dashboard: streamlit run app.py")

if __name__ == "__main__":
    main()

