# Project Explanation: Stock Analysis System

## 📋 What I've Built

I've created a **complete stock analysis platform** with three different ways to use it:

1. **Jupyter Notebook** - For learning and step-by-step analysis
2. **Streamlit Dashboard (Web App)** - Interactive web interface
3. **CLI Tool** - Command-line for automated reports

---

## 🏗️ Architecture Overview

### Core Modules (`src/` folder)

The project is organized into 4 main Python modules:

#### 1. `data_loader.py` - Data Fetching
- **Purpose**: Downloads stock price data from Yahoo Finance
- **Key Function**: `fetch_prices(tickers, start, end)`
- **How it works**: Uses `yfinance` library to download historical adjusted close prices
- **Output**: Pandas DataFrame with dates as index, stock tickers as columns

#### 2. `indicators.py` - Data Cleaning & Basic Metrics
- **Purpose**: Cleans data and calculates basic indicators
- **Key Functions**:
  - `prepare_prices()` - Forward-fills missing values, removes bad data
  - `rolling_mean()` - Calculates moving averages
  - `rolling_volatility()` - Calculates rolling standard deviation
  - `max_drawdown()` - Finds worst peak-to-trough decline

#### 3. `analysis.py` - Core Financial Calculations
- **Purpose**: Computes all financial metrics
- **Key Functions**:
  - `compute_daily_returns()` - Calculates daily percentage changes
  - `compute_cumulative_returns()` - Builds equity curves over time
  - `annual_metrics()` - Calculates annualized return, volatility, Sharpe ratio
  - Uses NumPy for mathematical computations

#### 4. `visualizations.py` - Chart Generation
- **Purpose**: Creates publication-ready charts
- **Generates**: Equity curves, performance comparisons, volatility charts, drawdown visualizations

---

## 🌐 How the Streamlit Dashboard Works

The dashboard (`app.py`) is an **interactive web application** built with Streamlit. Here's how it works:

### **User Interface Layout**

```
┌─────────────────────────────────────────┐
│  Sidebar (Left)    │  Main Area (Right) │
│                     │                    │
│  [Controls]         │  [Results]         │
│  - Ticker input     │  - Statistics      │
│  - Date pickers     │  - Charts          │
│  - Settings         │  - Downloads       │
│  - Analyze button   │                    │
└─────────────────────────────────────────┘
```

### **Step-by-Step Workflow**

#### **Step 1: User Input (Sidebar)**
When you open the dashboard, you see controls in the left sidebar:

1. **Stock Tickers Input**:
   - Text box where you enter comma-separated tickers
   - Default: "AAPL, MSFT, GOOGL, AMZN, TSLA"
   - Example: "AAPL, TSLA, NVDA"

2. **Date Range Pickers**:
   - Start Date: Calendar widget (default: 2018-01-01)
   - End Date: Calendar widget (default: today)

3. **Risk-Free Rate**:
   - Number input slider (0.0 to 1.0)
   - Used for Sharpe ratio calculation
   - Default: 0.0 (no risk-free rate)

4. **Rolling Window**:
   - Slider for rolling statistics (5-252 days)
   - Default: 20 days

5. **"Analyze" Button**:
   - Triggers the entire analysis pipeline

#### **Step 2: Processing (When "Analyze" is Clicked)**

Behind the scenes, the dashboard executes this pipeline:

```python
# 1. Fetch Data
prices_raw = fetch_prices(tickers, start, end)
# Downloads from Yahoo Finance via yfinance library

# 2. Clean Data
prices_clean = prepare_prices(prices_raw)
# Forward-fills gaps, removes bad rows

# 3. Calculate Returns
daily_returns = compute_daily_returns(prices_clean)
# Formula: r_t = (P_t / P_{t-1}) - 1

cum_returns = compute_cumulative_returns(daily_returns)
# Formula: cumprod(1 + daily_returns) - 1

# 4. Compute Metrics (using NumPy)
stats = annual_metrics(daily_returns, rf=risk_free_rate)
# Calculates:
#   - Annual Return = mean_daily * 252
#   - Annual Volatility = std_daily * sqrt(252)
#   - Sharpe Ratio = (return - rf) / volatility

# 5. Rolling Statistics
rolling_vol = rolling_volatility_annualized(daily_returns, window)
```

#### **Step 3: Display Results (Main Area)**

The results appear in the main area:

**A. Summary Statistics Table**
- Shows all metrics in a formatted DataFrame
- Columns: Annual Return, Annual Volatility, Sharpe Ratio, Max Drawdown
- Formatted as percentages for readability

**B. Key Findings Cards**
- Four metric cards showing:
  - **Top Return**: Stock with highest annualized return
  - **Best Sharpe**: Best risk-adjusted return
  - **Lowest Vol**: Most stable stock
  - **Worst DD**: Largest peak-to-trough decline

**C. Interactive Charts** (5 visualizations)

1. **Equity Curves**
   - Line chart showing cumulative returns over time
   - Each stock is a different colored line
   - Shows how $1 invested would grow over time

2. **Performance Metrics**
   - Two side-by-side bar charts
   - Left: Annualized Returns (horizontal bars)
   - Right: Annualized Volatility (horizontal bars)
   - Allows easy comparison

3. **Rolling Volatility**
   - Time-series line chart
   - Shows how volatility changes over time
   - Shaded areas highlight high-volatility periods
   - Useful for identifying market stress periods

4. **Drawdown Analysis**
   - Stacked charts (one per stock)
   - Shows drawdowns from peak values
   - Red shaded areas = periods of decline
   - Helps identify risk periods

5. **Sharpe Ratio Comparison**
   - Horizontal bar chart
   - Green bars = positive Sharpe (good risk-adjusted return)
   - Red bars = negative Sharpe (poor risk-adjusted return)
   - Dashed line at Sharpe = 1 (benchmark)

**D. Download Button**
- Allows users to download the summary statistics as CSV

### **Technical Details: How Streamlit Works**

Streamlit uses a **reactive programming model**:

1. **Session State**: Results are stored in `st.session_state` after computation
   - This prevents re-running calculations on every interaction
   - Data persists until user clicks "Analyze" again

2. **Widget Interaction**:
   - When user changes inputs → nothing happens until "Analyze" is clicked
   - This prevents excessive API calls to Yahoo Finance

3. **Error Handling**:
   - Try-except blocks catch errors (invalid tickers, date issues, etc.)
   - Error messages display in red boxes
   - Full exception traceback shown for debugging

4. **Plot Display**:
   - Matplotlib figures are generated using our visualization functions
   - `st.pyplot(fig)` renders them in the web interface
   - `plt.close(fig)` prevents memory leaks

---

## 🔬 The Math Behind It All

### Daily Returns
```
r_t = (P_t / P_{t-1}) - 1
```
- Example: If AAPL goes from $150 to $155, return = (155/150) - 1 = 3.33%

### Cumulative Returns
```
Cumulative = np.prod(1 + daily_returns) - 1
```
- Multiplies all (1 + daily return) values together
- Example: If daily returns are [0.01, 0.02, -0.01], cumulative = (1.01 * 1.02 * 0.99) - 1

### Annualized Return
```
Annual Return = mean(daily_returns) × 252
```
- Scales daily average by trading days per year
- Example: If average daily return is 0.1%, annual ≈ 25.2%

### Annualized Volatility
```
Annual Vol = std(daily_returns) × √252
```
- Standard deviation of daily returns, scaled by √252
- Measures risk/spread of returns

### Sharpe Ratio
```
Sharpe = (Annual Return - Risk-Free Rate) / Annual Volatility
```
- Risk-adjusted return metric
- Higher = better (more return per unit of risk)
- Sharpe > 1 is considered good, > 2 is excellent

---

## 🎯 Use Cases

### For Learning (Jupyter Notebook)
- Step-by-step explanation
- Can modify code cells
- See intermediate results
- Best for understanding the process

### For Quick Analysis (Streamlit Dashboard)
- Interactive, no coding required
- Fast results with visual feedback
- Good for comparing different stocks
- Shareable web interface

### For Automation (CLI Tool)
- Batch processing multiple analyses
- Integrate into scripts
- Generate reports on schedule
- Good for data pipelines

---

## 📊 Example Workflow

1. **User opens dashboard** → Sees default configuration
2. **User enters tickers**: "AAPL, TSLA, NVDA"
3. **User selects dates**: 2020-01-01 to 2024-12-31
4. **User clicks "Analyze"** → Spinner shows "Fetching data..."
5. **System downloads data** from Yahoo Finance (3-5 seconds)
6. **System processes data**:
   - Cleans: removes missing values
   - Calculates: returns, metrics (1-2 seconds)
   - Generates: charts (1-2 seconds)
7. **Results appear**:
   - Statistics table shows TSLA had highest return but also highest volatility
   - Charts visualize the differences
   - User can download CSV of results

---

## 🔧 Technical Stack

- **Backend**: Python 3.9+
- **Data**: Pandas (data manipulation), NumPy (math)
- **Data Source**: yfinance (Yahoo Finance API wrapper)
- **Visualization**: Matplotlib, Seaborn
- **Web Framework**: Streamlit
- **Notebook**: Jupyter

---

## 💡 Key Features

1. **Modular Design**: Each module has a single responsibility
2. **Reusable Functions**: Can be used in notebooks, scripts, or dashboard
3. **Error Handling**: Graceful handling of bad data/invalid inputs
4. **Professional Output**: Publication-ready charts and formatted tables
5. **Multiple Interfaces**: Choose the tool that fits your workflow

---

## 🚀 Running the Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

The dashboard will:
- Start a local web server
- Open in your browser automatically
- Default URL: http://localhost:8501

---

This system provides a complete, production-ready stock analysis tool that can be used for portfolio analysis, research, or as a portfolio project demonstrating data science and financial analysis skills.

