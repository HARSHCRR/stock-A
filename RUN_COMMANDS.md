# ✅ Ready to Run! - Commands Reference

## 🎯 Quick Start (3 Steps)

### Step 1: Activate Virtual Environment
```bash
source venv/bin/activate
```
*(You'll see `(venv)` appear in your terminal prompt)*

### Step 2: Choose Your Interface

**Option A: Streamlit Dashboard (Easiest - Web Interface)**
```bash
streamlit run app.py
```
Then open your browser to the URL shown (usually http://localhost:8501)

**Option B: Jupyter Notebook (For Learning)**
```bash
jupyter notebook notebooks/stock_analysis.ipynb
```

**Option C: CLI Report (For Quick Analysis)**
```bash
python cli_report.py AAPL MSFT GOOGL AMZN TSLA
```

---

## 📋 Complete Command Examples

### Test Installation
```bash
source venv/bin/activate
python example.py
```

### Run Dashboard
```bash
source venv/bin/activate
streamlit run app.py
```

### Run CLI with Custom Dates
```bash
source venv/bin/activate
python cli_report.py AAPL TSLA --start 2020-01-01 --rf 0.02
```

### Run Notebook
```bash
source venv/bin/activate
jupyter notebook notebooks/stock_analysis.ipynb
```

---

## ⚠️ Important Notes

1. **Always activate venv first** - `source venv/bin/activate`
2. **Don't copy `#` lines** - Those are comments, not commands
3. **Use `python` not `python3`** - After activating venv, `python` works
4. **Dashboard opens automatically** - Just wait for the browser

---

## 🐛 Troubleshooting

**"command not found" errors?**
- Make sure you activated venv: `source venv/bin/activate`
- Check you're in the project directory: `cd /Users/gunjanshrivastava/Documents/projext`

**Dashboard won't open?**
- Wait a few seconds for Streamlit to start
- Check the terminal for the URL (usually http://localhost:8501)
- Manually open that URL in your browser

**Data download errors?**
- Check your internet connection
- Verify ticker symbols are correct (e.g., "AAPL" not "apple")

---

## ✅ Verification

The example script ran successfully! You should see:
- ✅ Data fetched successfully
- ✅ Metrics calculated
- ✅ Output showing AAPL and MSFT statistics

Your setup is complete and working! 🎉

