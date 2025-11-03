#!/usr/bin/env python3
"""
CLI Report Generator for Stock Analysis
"""
import argparse
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import fetch_prices, save_raw_data
from indicators import prepare_prices, max_drawdown
from analysis import (
    compute_daily_returns,
    compute_cumulative_returns,
    annual_metrics,
    rolling_volatility_annualized,
    prepare_returns
)
from visualizations import create_summary_charts


def generate_report(tickers, start_date, end_date, risk_free_rate, output_dir):
    """
    Generate comprehensive stock analysis report.
    
    Parameters:
    -----------
    tickers : list
        List of ticker symbols
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str or None
        End date in YYYY-MM-DD format
    risk_free_rate : float
        Risk-free rate for Sharpe ratio calculation
    output_dir : str
        Output directory for reports
    """
    print("=" * 80)
    print("STOCK ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTickers: {', '.join(tickers)}")
    print(f"Date Range: {start_date} to {'Today' if end_date is None else end_date}")
    print(f"Risk-Free Rate: {risk_free_rate:.3%}")
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'charts'), exist_ok=True)
    
    print("\n" + "-" * 80)
    print("1. FETCHING DATA")
    print("-" * 80)
    prices_raw = fetch_prices(tickers, start=start_date, end=end_date)
    print(f"   Fetched {len(prices_raw)} days of data")
    
    # Save raw data
    save_raw_data(prices_raw, output_dir=os.path.join(output_dir, 'data'), 
                  filename='raw_prices.csv')
    
    print("\n" + "-" * 80)
    print("2. CLEANING DATA")
    print("-" * 80)
    prices_clean = prepare_prices(prices_raw)
    print(f"   Clean data shape: {prices_clean.shape}")
    print(f"   Missing values: {prices_clean.isna().sum().sum()} total")
    
    # Save clean data
    prices_clean.to_csv(os.path.join(output_dir, 'data', 'clean_prices.csv'))
    
    print("\n" + "-" * 80)
    print("3. COMPUTING RETURNS")
    print("-" * 80)
    daily_returns = compute_daily_returns(prices_clean)
    cum_returns = compute_cumulative_returns(daily_returns)
    print(f"   Daily returns computed: {daily_returns.shape}")
    print(f"   Cumulative returns computed: {cum_returns.shape}")
    
    print("\n" + "-" * 80)
    print("4. ANNUALIZED METRICS")
    print("-" * 80)
    stats = annual_metrics(daily_returns, rf=risk_free_rate)
    max_dd = max_drawdown(prices_clean)
    stats['max_drawdown'] = max_dd
    
    # Display stats
    print("\nSummary Statistics:")
    print(stats.round(4))
    
    # Save stats
    stats.to_csv(os.path.join(output_dir, 'data', 'summary_stats.csv'))
    print(f"\n   Saved to {output_dir}/data/summary_stats.csv")
    
    print("\n" + "-" * 80)
    print("5. KEY FINDINGS")
    print("-" * 80)
    top_return = stats['annual_return'].idxmax()
    best_sharpe = stats['sharpe'].idxmax()
    lowest_vol = stats['annual_vol'].idxmin()
    worst_dd = stats['max_drawdown'].idxmin()
    
    print(f"\n   Top Performer (Return): {top_return} ({stats.loc[top_return, 'annual_return']:.2%})")
    print(f"   Best Sharpe Ratio: {best_sharpe} ({stats.loc[best_sharpe, 'sharpe']:.4f})")
    print(f"   Lowest Volatility: {lowest_vol} ({stats.loc[lowest_vol, 'annual_vol']:.2%})")
    print(f"   Worst Drawdown: {worst_dd} ({stats.loc[worst_dd, 'max_drawdown']:.2%})")
    
    print("\n" + "-" * 80)
    print("6. GENERATING CHARTS")
    print("-" * 80)
    rolling_vol = rolling_volatility_annualized(daily_returns, window=20)
    create_summary_charts(prices_clean, daily_returns, cum_returns, rolling_vol, 
                         stats, output_dir=os.path.join(output_dir, 'charts'))
    
    print("\n" + "=" * 80)
    print("REPORT COMPLETE")
    print("=" * 80)
    print(f"\nAll outputs saved to: {output_dir}/")
    print(f"  - Data: {output_dir}/data/")
    print(f"  - Charts: {output_dir}/charts/")


def main():
    parser = argparse.ArgumentParser(
        description='Generate stock analysis report',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_report.py AAPL MSFT GOOGL --start 2020-01-01
  python cli_report.py AAPL MSFT --start 2018-01-01 --rf 0.02 --output reports/
        """
    )
    
    parser.add_argument('tickers', nargs='+', help='Stock ticker symbols (e.g., AAPL MSFT GOOGL)')
    parser.add_argument('--start', default='2018-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default=None, help='End date (YYYY-MM-DD), default: today')
    parser.add_argument('--rf', type=float, default=0.0, help='Risk-free rate (default: 0.0)')
    parser.add_argument('--output', default='reports', help='Output directory (default: reports)')
    
    args = parser.parse_args()
    
    generate_report(
        tickers=args.tickers,
        start_date=args.start,
        end_date=args.end,
        risk_free_rate=args.rf,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()

