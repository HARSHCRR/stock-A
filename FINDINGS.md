# Stock Analysis Findings Summary

## Project Objective
Analyze historical stock price data for 5 major tech stocks to compute returns, volatility, and risk-adjusted performance metrics.

## Methodology
1. **Data Acquisition**: Fetched historical adjusted close prices using yfinance (2018-2024)
2. **Data Cleaning**: Forward-filled missing values, aligned trading days
3. **Returns Calculation**: 
   - Daily returns: `r_t = (P_t / P_{t-1}) - 1`
   - Cumulative returns: `np.prod(1 + daily_returns) - 1`
4. **Annualized Metrics** (252 trading days/year):
   - Annualized Return: `mean_daily * 252`
   - Annualized Volatility: `std_daily * sqrt(252)`
   - Sharpe Ratio: `(annual_return - rf) / annual_vol`
5. **Rolling Statistics**: 20-day rolling window for mean and volatility
6. **Risk Metrics**: Maximum drawdown from peak values

## Key Findings

*Note: Run the analysis to generate actual findings based on real data.*

### Performance Rankings
1. **Top Performer (Highest Annual Return)**: [Ticker]
2. **Best Sharpe Ratio (Risk-Adjusted)**: [Ticker]
3. **Lowest Volatility (Most Stable)**: [Ticker]
4. **Worst Drawdown**: [Ticker]

### Insights
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]

## Sample Equity Curve
*See `slides/equity_curves.png` for the complete visualization*

## Methodology Notes
- Risk-free rate assumption: 0% (can be adjusted)
- Trading days per year: 252
- Rolling window: 20 days
- Data source: Yahoo Finance via yfinance

---

*To generate findings for your specific stocks and date range, run the Jupyter notebook or CLI report.*

