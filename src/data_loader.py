"""
Data loading module for fetching historical stock price data.
"""
import yfinance as yf
import pandas as pd
import os
from pathlib import Path


def fetch_prices(tickers, start='2018-01-01', end=None):
    """
    Fetch historical price data for given tickers.
    
    Parameters:
    -----------
    tickers : list or str
        List of ticker symbols or single ticker string
    start : str
        Start date in 'YYYY-MM-DD' format
    end : str or None
        End date in 'YYYY-MM-DD' format. If None, uses today's date.
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with adjusted close prices (columns = tickers, index = dates)
    """
    # Download data - don't use auto_adjust to get Adj Close column explicitly
    data = yf.download(tickers, start=start, end=end, progress=False)
    
    # Handle different response structures
    ticker_list = tickers if isinstance(tickers, list) else [tickers]
    
    # Extract Adjusted Close prices
    if isinstance(data.columns, pd.MultiIndex):
        # MultiIndex structure (Open, High, Low, Close, Adj Close, Volume)
        if 'Adj Close' in data.columns.levels[0]:
            df = data['Adj Close'].copy()
        else:
            # Fallback to Close if Adj Close not available
            df = data['Close'].copy()
    elif isinstance(data, pd.DataFrame):
        # Single ticker - might be flat structure
        if 'Adj Close' in data.columns:
            df = data[['Adj Close']].copy()
        elif 'Close' in data.columns:
            df = data[['Close']].copy()
        else:
            # Use first column (should be Close/Adj Close)
            df = data.iloc[:, 0:1].copy()
    else:
        # If it's a Series, convert to DataFrame
        df = data.to_frame()
    
    # Ensure column names match tickers
    if isinstance(df, pd.DataFrame):
        if len(df.columns) == len(ticker_list):
            df.columns = ticker_list
        elif len(df.columns) == 1 and len(ticker_list) == 1:
            df.columns = [ticker_list[0]]
        # If columns don't match, keep original names
    
    return df


def save_raw_data(df, output_dir='data', filename='raw_prices.csv'):
    """
    Save raw price data to CSV.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Price data to save
    output_dir : str
        Output directory path
    filename : str
        Output filename
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath)
    print(f"Raw data saved to {filepath}")


def load_raw_data(filepath='data/raw_prices.csv'):
    """
    Load raw price data from CSV.
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file
    
    Returns:
    --------
    pd.DataFrame
        Price data with date index
    """
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return df


if __name__ == "__main__":
    # Example usage
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    print("Fetching price data...")
    prices = fetch_prices(tickers, start='2018-01-01')
    print(f"\nFetched {len(prices)} days of data")
    print(prices.head())
    save_raw_data(prices)

