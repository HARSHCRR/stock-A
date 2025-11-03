"""
Visualization module for creating charts and plots.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Set style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
sns.set_palette("husl")


def plot_equity_curves(cum_returns, save_path=None, title="Equity Curves"):
    """
    Plot cumulative returns (equity curves) for all tickers.
    
    Parameters:
    -----------
    cum_returns : pd.DataFrame
        Cumulative returns data
    save_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for col in cum_returns.columns:
        ax.plot(cum_returns.index, cum_returns[col], label=col, linewidth=2)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Return', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved equity curves to {save_path}")
    
    return fig, ax


def plot_performance_table(stats, save_path=None, title="Performance Metrics"):
    """
    Create bar charts for annualized return and volatility.
    
    Parameters:
    -----------
    stats : pd.DataFrame
        Summary statistics with annual_return and annual_vol columns
    save_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Annualized Return
    stats_sorted_return = stats.sort_values('annual_return', ascending=True)
    ax1.barh(stats_sorted_return.index, stats_sorted_return['annual_return'], 
             color='green', alpha=0.7)
    ax1.set_xlabel('Annualized Return', fontsize=12)
    ax1.set_title('Annualized Return', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Annualized Volatility
    stats_sorted_vol = stats.sort_values('annual_vol', ascending=True)
    ax2.barh(stats_sorted_vol.index, stats_sorted_vol['annual_vol'],
             color='red', alpha=0.7)
    ax2.set_xlabel('Annualized Volatility', fontsize=12)
    ax2.set_title('Annualized Volatility', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved performance table to {save_path}")
    
    return fig, (ax1, ax2)


def plot_rolling_volatility(rolling_vol, save_path=None, title="Rolling Volatility (Annualized)"):
    """
    Plot rolling volatility with shaded volatility spikes.
    
    Parameters:
    -----------
    rolling_vol : pd.DataFrame
        Rolling volatility data
    save_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate mean volatility for shading
    mean_vol = rolling_vol.mean(axis=1)
    std_vol = rolling_vol.std(axis=1)
    
    # Shade high volatility periods (above mean + 1 std)
    high_vol_threshold = mean_vol + std_vol
    ax.fill_between(rolling_vol.index, 0, high_vol_threshold.values,
                    where=(mean_vol.values > mean_vol.mean()),
                    alpha=0.2, color='red', label='High Volatility Periods')
    
    # Plot rolling volatility for each ticker
    for col in rolling_vol.columns:
        ax.plot(rolling_vol.index, rolling_vol[col], label=col, linewidth=2, alpha=0.7)
    
    # Plot mean volatility line
    ax.plot(rolling_vol.index, mean_vol, color='black', linestyle='--',
            linewidth=2, label='Mean Volatility', alpha=0.8)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Annualized Volatility', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved rolling volatility chart to {save_path}")
    
    return fig, ax


def plot_max_drawdown(prices, save_path=None, title="Drawdown Analysis"):
    """
    Visualize drawdowns from peaks.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        Price data
    save_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, axes = plt.subplots(len(prices.columns), 1, figsize=(12, 4 * len(prices.columns)))
    
    if len(prices.columns) == 1:
        axes = [axes]
    
    for idx, col in enumerate(prices.columns):
        price_series = prices[col]
        roll_max = price_series.cummax()
        drawdown = (price_series - roll_max) / roll_max
        
        axes[idx].fill_between(drawdown.index, 0, drawdown.values,
                              color='red', alpha=0.3, label='Drawdown')
        axes[idx].plot(drawdown.index, drawdown.values, color='darkred', linewidth=1.5)
        axes[idx].set_ylabel(f'{col} Drawdown', fontsize=10)
        axes[idx].set_title(f'{col} - Maximum Drawdown: {drawdown.min():.2%}', 
                           fontsize=11, fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
        axes[idx].legend(loc='best')
    
    axes[-1].set_xlabel('Date', fontsize=12)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved drawdown chart to {save_path}")
    
    return fig, axes


def plot_sharpe_ratios(stats, save_path=None, title="Sharpe Ratio Comparison"):
    """
    Plot Sharpe ratios as a bar chart.
    
    Parameters:
    -----------
    stats : pd.DataFrame
        Summary statistics with sharpe column
    save_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    stats_sorted = stats.sort_values('sharpe', ascending=True)
    colors = ['green' if x > 0 else 'red' for x in stats_sorted['sharpe']]
    
    ax.barh(stats_sorted.index, stats_sorted['sharpe'], color=colors, alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=1, color='blue', linestyle='--', linewidth=1, alpha=0.5, label='Sharpe = 1')
    ax.set_xlabel('Sharpe Ratio', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved Sharpe ratio chart to {save_path}")
    
    return fig, ax


def create_summary_charts(prices, daily_returns, cum_returns, rolling_vol, stats, output_dir='slides'):
    """
    Create all summary charts and save them.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        Price data
    daily_returns : pd.DataFrame
        Daily returns
    cum_returns : pd.DataFrame
        Cumulative returns
    rolling_vol : pd.DataFrame
        Rolling volatility
    stats : pd.DataFrame
        Summary statistics
    output_dir : str
        Directory to save charts
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    plot_equity_curves(cum_returns, save_path=f'{output_dir}/equity_curves.png')
    plot_performance_table(stats, save_path=f'{output_dir}/performance_metrics.png')
    plot_rolling_volatility(rolling_vol, save_path=f'{output_dir}/rolling_volatility.png')
    plot_max_drawdown(prices, save_path=f'{output_dir}/max_drawdown.png')
    plot_sharpe_ratios(stats, save_path=f'{output_dir}/sharpe_ratios.png')
    
    print(f"\nAll charts saved to {output_dir}/")

