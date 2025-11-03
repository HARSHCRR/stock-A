"""
Streamlit Dashboard for Stock Analysis
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import fetch_prices
from indicators import prepare_prices, max_drawdown
from analysis import (
    compute_daily_returns,
    compute_cumulative_returns,
    annual_metrics,
    rolling_volatility_annualized,
    prepare_returns
)
from visualizations import (
    plot_equity_curves,
    plot_performance_table,
    plot_rolling_volatility,
    plot_max_drawdown,
    plot_sharpe_ratios
)

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Analysis Dashboard")
st.markdown("Analyze historical stock prices, returns, volatility, and risk metrics")

# Sidebar for inputs
st.sidebar.header("Configuration")

# Ticker input
default_tickers = "AAPL, MSFT, GOOGL, AMZN, TSLA"
ticker_input = st.sidebar.text_input(
    "Stock Tickers (comma-separated)",
    value=default_tickers
)
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

# Date range
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", value=pd.to_datetime('2018-01-01').date())
end_date = col2.date_input("End Date", value=None)

# Risk-free rate
risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate (annualized)",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.001,
    format="%.3f"
)

# Rolling window
rolling_window = st.sidebar.slider("Rolling Window (days)", min_value=5, max_value=252, value=20)

if st.sidebar.button("Analyze"):
    if len(tickers) == 0:
        st.error("Please enter at least one ticker symbol")
    else:
        with st.spinner("Fetching data and computing metrics..."):
            try:
                # Fetch data
                end_str = end_date.strftime('%Y-%m-%d') if end_date else None
                start_str = start_date.strftime('%Y-%m-%d')
                
                prices_raw = fetch_prices(tickers, start=start_str, end=end_str)
                
                if prices_raw.empty:
                    st.error("No data fetched. Please check ticker symbols and date range.")
                else:
                    # Clean data
                    prices_clean = prepare_prices(prices_raw)
                    
                    # Compute returns
                    daily_returns = compute_daily_returns(prices_clean)
                    cum_returns = compute_cumulative_returns(daily_returns)
                    
                    # Compute metrics
                    stats = annual_metrics(daily_returns, rf=risk_free_rate)
                    max_dd = max_drawdown(prices_clean)
                    stats['max_drawdown'] = max_dd
                    
                    # Rolling statistics
                    rolling_vol = rolling_volatility_annualized(daily_returns, window=rolling_window)
                    
                    # Store in session state
                    st.session_state['prices_clean'] = prices_clean
                    st.session_state['daily_returns'] = daily_returns
                    st.session_state['cum_returns'] = cum_returns
                    st.session_state['stats'] = stats
                    st.session_state['rolling_vol'] = rolling_vol
                    st.session_state['tickers'] = tickers
                    
                    st.success(f"Successfully analyzed {len(tickers)} stocks")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.exception(e)

# Display results if available
if 'stats' in st.session_state:
    stats = st.session_state['stats']
    prices_clean = st.session_state['prices_clean']
    daily_returns = st.session_state['daily_returns']
    cum_returns = st.session_state['cum_returns']
    rolling_vol = st.session_state['rolling_vol']
    tickers = st.session_state['tickers']
    
    # Summary statistics
    st.header("Summary Statistics")
    
    # Format stats for display
    stats_display = stats.copy()
    for col in ['annual_return', 'annual_vol', 'total_return', 'max_drawdown']:
        if col in stats_display.columns:
            stats_display[col] = stats_display[col].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
    
    st.dataframe(stats_display, use_container_width=True)
    
    # Key findings
    st.header("Key Findings")
    col1, col2, col3, col4 = st.columns(4)
    
    top_return = stats['annual_return'].idxmax()
    best_sharpe = stats['sharpe'].idxmax()
    lowest_vol = stats['annual_vol'].idxmin()
    worst_dd = stats['max_drawdown'].idxmin()
    
    col1.metric("Top Return", top_return, f"{stats.loc[top_return, 'annual_return']:.2%}")
    col2.metric("Best Sharpe", best_sharpe, f"{stats.loc[best_sharpe, 'sharpe']:.4f}")
    col3.metric("Lowest Vol", lowest_vol, f"{stats.loc[lowest_vol, 'annual_vol']:.2%}")
    col4.metric("Worst DD", worst_dd, f"{stats.loc[worst_dd, 'max_drawdown']:.2%}")
    
    # Charts
    st.header("Visualizations")
    
    # Equity curves
    st.subheader("Equity Curves")
    fig, _ = plot_equity_curves(cum_returns)
    st.pyplot(fig)
    plt.close(fig)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    fig, _ = plot_performance_table(stats)
    st.pyplot(fig)
    plt.close(fig)
    
    # Rolling volatility
    st.subheader("Rolling Volatility")
    fig, _ = plot_rolling_volatility(rolling_vol)
    st.pyplot(fig)
    plt.close(fig)
    
    # Drawdown
    st.subheader("Drawdown Analysis")
    fig, _ = plot_max_drawdown(prices_clean)
    st.pyplot(fig)
    plt.close(fig)
    
    # Sharpe ratios
    st.subheader("Sharpe Ratios")
    fig, _ = plot_sharpe_ratios(stats)
    st.pyplot(fig)
    plt.close(fig)
    
    # Download button
    st.header("Download Results")
    csv = stats.to_csv()
    st.download_button(
        label="Download Summary Statistics (CSV)",
        data=csv,
        file_name="summary_stats.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Use the sidebar to configure analysis parameters and click 'Analyze' to begin.")

