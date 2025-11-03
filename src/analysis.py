"""
Core analytics module for computing returns, volatility, and risk metrics.
"""
import pandas as pd
import numpy as np


def compute_daily_returns(prices):
    """
    Compute daily returns from price data.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        Price data with date index
    
    Returns:
    --------
    pd.DataFrame
        Daily returns (percentage change)
    """
    daily_returns = prices.pct_change().dropna()
    return daily_returns


def compute_cumulative_returns(daily_returns):
    """
    Compute cumulative returns from daily returns.
    
    Parameters:
    -----------
    daily_returns : pd.DataFrame
        Daily returns data
    
    Returns:
    --------
    pd.DataFrame
        Cumulative returns over time
    """
    cum_returns = (1 + daily_returns).cumprod() - 1
    return cum_returns


def annual_metrics(daily_returns, rf=0.0, trading_days=252):
    """
    Compute annualized return, volatility, and Sharpe ratio.
    
    Parameters:
    -----------
    daily_returns : pd.DataFrame
        Daily returns data
    rf : float
        Risk-free rate (annualized)
    trading_days : int
        Number of trading days per year (default: 252)
    
    Returns:
    --------
    pd.DataFrame
        Summary statistics for each ticker
    """
    stats = {}
    
    for col in daily_returns.columns:
        arr = daily_returns[col].values
        
        # Filter out NaN values
        arr = arr[~np.isnan(arr)]
        
        if len(arr) == 0:
            stats[col] = {
                'annual_return': np.nan,
                'annual_vol': np.nan,
                'sharpe': np.nan,
                'total_return': np.nan
            }
            continue
        
        # Mean daily return
        mean_daily = np.mean(arr)
        
        # Annualized return
        ann_return = mean_daily * trading_days
        
        # Annualized volatility (using population std, ddof=0)
        ann_vol = np.std(arr, ddof=0) * np.sqrt(trading_days)
        
        # Sharpe ratio
        if ann_vol != 0:
            sharpe = (ann_return - rf) / ann_vol
        else:
            sharpe = np.nan
        
        # Total return over the period
        total_return = np.prod(1 + arr) - 1
        
        stats[col] = {
            'annual_return': ann_return,
            'annual_vol': ann_vol,
            'sharpe': sharpe,
            'total_return': total_return
        }
    
    return pd.DataFrame(stats).T


def rolling_volatility_annualized(daily_returns, window=20, trading_days=252):
    """
    Compute annualized rolling volatility.
    
    Parameters:
    -----------
    daily_returns : pd.DataFrame
        Daily returns data
    window : int
        Rolling window size in days
    trading_days : int
        Number of trading days per year
    
    Returns:
    --------
    pd.DataFrame
        Annualized rolling volatility
    """
    rolling_vol = daily_returns.rolling(window=window).std() * np.sqrt(trading_days)
    return rolling_vol


def rolling_mean_returns(daily_returns, window=20, trading_days=252):
    """
    Compute annualized rolling mean returns.
    
    Parameters:
    -----------
    daily_returns : pd.DataFrame
        Daily returns data
    window : int
        Rolling window size in days
    trading_days : int
        Number of trading days per year
    
    Returns:
    --------
    pd.DataFrame
        Annualized rolling mean returns
    """
    rolling_mean = daily_returns.rolling(window=window).mean() * trading_days
    return rolling_mean


def prepare_returns(prices):
    """
    Prepare returns from price data (complete pipeline).
    
    Parameters:
    -----------
    prices : pd.DataFrame
        Clean price data
    
    Returns:
    --------
    tuple
        (prices, daily_returns, cum_returns)
    """
    # Ensure sorted by date
    prices = prices.sort_index()
    
    # Forward fill small gaps and drop rows where all are NaN
    prices = prices.ffill().dropna(how='all')
    
    # Compute daily returns
    daily_returns = compute_daily_returns(prices)
    
    # Compute cumulative returns
    cum_returns = compute_cumulative_returns(daily_returns)
    
    return prices, daily_returns, cum_returns


def compute_summary_stats(prices, daily_returns, rf=0.0):
    """
    Compute comprehensive summary statistics.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        Price data
    daily_returns : pd.DataFrame
        Daily returns data
    rf : float
        Risk-free rate
    
    Returns:
    --------
    pd.DataFrame
        Summary statistics including annualized metrics and max drawdown
    """
    # Annualized metrics
    stats = annual_metrics(daily_returns, rf=rf)
    
    # Max drawdown
    max_dd = max_drawdown(prices)
    stats['max_drawdown'] = max_dd
    
    return stats


if __name__ == "__main__":
    # Example usage
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import fetch_prices
    from src.indicators import prepare_prices
    
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    prices = fetch_prices(tickers, start='2020-01-01')
    clean_prices = prepare_prices(prices)
    
    prices_clean, daily_returns, cum_returns = prepare_returns(clean_prices)
    
    print("Daily Returns (last 5 days):")
    print(daily_returns.tail())
    print("\nCumulative Returns (last 5 days):")
    print(cum_returns.tail())
    print("\nAnnualized Metrics:")
    stats = annual_metrics(daily_returns)
    print(stats)

