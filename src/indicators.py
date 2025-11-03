"""
Technical indicators and rolling statistics module.
"""
import pandas as pd
import numpy as np


def rolling_mean(data, window=20):
    """
    Calculate rolling mean.
    
    Parameters:
    -----------
    data : pd.Series or pd.DataFrame
        Input data
    window : int
        Rolling window size in days
    
    Returns:
    --------
    pd.Series or pd.DataFrame
        Rolling mean values
    """
    return data.rolling(window=window).mean()


def rolling_volatility(data, window=20):
    """
    Calculate rolling volatility (standard deviation).
    
    Parameters:
    -----------
    data : pd.Series or pd.DataFrame
        Input data
    window : int
        Rolling window size in days
    
    Returns:
    --------
    pd.Series or pd.DataFrame
        Rolling volatility values
    """
    return data.rolling(window=window).std()


def max_drawdown(prices):
    """
    Calculate maximum drawdown for a price series.
    
    Parameters:
    -----------
    prices : pd.Series or pd.DataFrame
        Price data
    
    Returns:
    --------
    pd.Series
        Maximum drawdown for each column
    """
    if isinstance(prices, pd.Series):
        roll_max = prices.cummax()
        drawdown = (prices - roll_max) / roll_max
        return drawdown.min()
    else:
        # For DataFrame, calculate for each column
        drawdowns = {}
        for col in prices.columns:
            roll_max = prices[col].cummax()
            drawdown = (prices[col] - roll_max) / roll_max
            drawdowns[col] = drawdown.min()
        return pd.Series(drawdowns)


def prepare_prices(df):
    """
    Clean and prepare price data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw price data
    
    Returns:
    --------
    pd.DataFrame
        Clean price data with forward-filled missing values
    """
    # Sort by date
    df = df.sort_index()
    
    # Forward fill small gaps, then drop rows where all values are NaN
    df = df.ffill().dropna(how='all')
    
    # Optionally, drop rows with too many NaN values (e.g., if more than 50% are NaN)
    threshold = len(df.columns) * 0.5
    df = df.dropna(thresh=threshold)
    
    return df


if __name__ == "__main__":
    # Example usage
    import yfinance as yf
    tickers = ['AAPL', 'MSFT']
    prices = yf.download(tickers, start='2020-01-01', progress=False)['Adj Close']
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()
        prices.columns = [tickers]
    
    clean_prices = prepare_prices(prices)
    print("Clean prices shape:", clean_prices.shape)
    print("\nRolling mean (20-day):")
    print(rolling_mean(clean_prices['AAPL'], window=20).tail())
    print("\nMax drawdown:")
    print(max_drawdown(clean_prices))

