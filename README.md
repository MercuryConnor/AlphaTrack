<div align="center">
  <h1>AlphaTrack</h1>
  <p><b>Stock Price Tracker & Trading Strategy Visualizer</b></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python"/>
    <img src="https://img.shields.io/badge/Streamlit-Enabled-red?logo=streamlit"/>
    <img src="https://img.shields.io/badge/Pandas-Data-green?logo=pandas"/>
    <img src="https://img.shields.io/badge/Matplotlib-Plotting-yellow?logo=matplotlib"/>
    <img src="https://img.shields.io/badge/yfinance-API-blueviolet"/>
  </p>
</div>

---


## 📸 Sample Screenshot

<div align="center">
  <img src="https://raw.githubusercontent.com/MercuryConnor/AlphaTrack/main/sample_screenshot.png" alt="AlphaTrack Sample Screenshot" width="600"/>
</div>

---

## 📈 What is AlphaTrack?

AlphaTrack is a web-based app to track live/historical stock prices, visualize trading strategies (like moving average crossovers), and analyze performance metrics—all in a simple Streamlit interface.

---

## � Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/AlphaTrack.git
cd AlphaTrack
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

---

## 🛠️ Architecture Overview

```
AlphaTrack/
├── app.py          # Streamlit UI & main logic
├── strategy.py     # Trading strategy logic (SMA crossover)
├── utils.py        # Helper functions (moving averages, etc.)
├── requirements.txt
├── README.md
├── .streamlit/     # Streamlit config for deployment
```

### Main Components
- **app.py**: Handles UI, user input, and visualization
- **strategy.py**: Contains SMA crossover logic and signal generation
- **utils.py**: Calculates moving averages and data cleaning

---

## 💡 Usage Example

1. Enter a stock symbol (e.g., `RELIANCE.NS`)
2. Select date range and moving average windows
3. Click "Fetch & Analyze" to see:
   - Price chart with buy/sell signals
   - Total return, number of trades, win rate

#### Code Example (SMA Crossover)
```python
from strategy import sma_crossover_signals
signals = sma_crossover_signals(data, short_window=20, long_window=50)
```

---

## 📚 API Guide

**sma_crossover_signals(data, short_window, long_window)**
- Returns buy/sell signals based on SMA crossover

**calculate_moving_averages(data, short_window, long_window)**
- Adds SMA columns to your DataFrame

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## � License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- [Streamlit](https://streamlit.io/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)

---

Happy learning and building!
