"""
Stock Analysis Package
"""
from .data_loader import fetch_prices, save_raw_data, load_raw_data
from .indicators import rolling_mean, rolling_volatility, max_drawdown, prepare_prices
from .analysis import (
    compute_daily_returns,
    compute_cumulative_returns,
    annual_metrics,
    rolling_volatility_annualized,
    rolling_mean_returns,
    prepare_returns,
    compute_summary_stats
)
from .visualizations import (
    plot_equity_curves,
    plot_performance_table,
    plot_rolling_volatility,
    plot_max_drawdown,
    plot_sharpe_ratios,
    create_summary_charts
)

__version__ = '1.0.0'

