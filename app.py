
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from strategy import sma_crossover_signals
from utils import calculate_moving_averages

st.title('AlphaTrack: Stock Price Tracker & Strategy Visualizer')

sample_symbols = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'META', 'NFLX', 'NVDA'
]
symbol = st.sidebar.selectbox('Stock Symbol (or type your own)', sample_symbols, index=0)
custom_symbol = st.sidebar.text_input('Or enter a custom symbol', '')
if custom_symbol.strip():
    symbol = custom_symbol.strip()
start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2022-01-01'))
end_date = st.sidebar.date_input('End Date', pd.to_datetime('today'))
short_window = st.sidebar.number_input('Short MA Window', min_value=1, value=20)
long_window = st.sidebar.number_input('Long MA Window', min_value=2, value=50)

if st.sidebar.button('Fetch & Analyze'):
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        st.error('No data found for the selected symbol and date range.')
    else:
        data = calculate_moving_averages(data, short_window, long_window)
        signals = sma_crossover_signals(data, short_window, long_window)
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(data.index, data['Close'], label='Close Price')
        ax.plot(data.index, data[f'SMA_{short_window}'], label=f'SMA {short_window}')
        ax.plot(data.index, data[f'SMA_{long_window}'], label=f'SMA {long_window}')
        # Plot buy/sell signals
        ax.plot(signals['Buy'].index, signals['Buy']['Close'], '^', markersize=10, color='g', label='Buy Signal')
        ax.plot(signals['Sell'].index, signals['Sell']['Close'], 'v', markersize=10, color='r', label='Sell Signal')
        ax.legend()
        st.pyplot(fig)
        # Basic performance
        # Safely get first and last close price for total return
        close_prices = data['Close'].values
        if len(close_prices) > 1:
            total_return = ((close_prices[-1] / close_prices[0]) - 1) * 100
            try:
                total_return_val = float(total_return)
                st.write(f"Total Return: {total_return_val:.2f}%")
            except Exception:
                st.write(f"Total Return: {total_return}%")
        else:
            st.write("Not enough data to calculate total return.")
        st.write(f"Number of Trades: {len(signals['Buy']) + len(signals['Sell'])}")
        # Win rate calculation
        buy_indices = signals['Buy'].index
        sell_indices = signals['Sell'].index
        # Only consider pairs where a buy is followed by a sell
        wins = 0
        total = 0
        for buy_time in buy_indices:
            # Find the first sell after this buy
            future_sells = [s for s in sell_indices if s > buy_time]
            if future_sells:
                sell_time = future_sells[0]
                buy_price = float(data.loc[buy_time, 'Close'])
                sell_price = float(data.loc[sell_time, 'Close'])
                if sell_price > buy_price:
                    wins += 1
                total += 1
        if total > 0:
            win_rate = (wins / total) * 100
            st.write(f"Win Rate: {win_rate:.2f}% ({wins}/{total})")
        else:
            st.write("Win Rate: Not enough completed trades to calculate.")
