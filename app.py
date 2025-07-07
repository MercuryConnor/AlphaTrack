
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


strategy_options = ['SMA Crossover', 'Bollinger Bands', 'RSI']
strategy_choice = st.sidebar.selectbox('Select Strategy', strategy_options)


# short_window = st.sidebar.number_input('Short MA Window', min_value=1, value=20)
#long_window = st.sidebar.number_input('Long MA Window', min_value=2, value=50)
#bb_window = st.sidebar.number_input('BB Window', min_value=1, value=20)
#bb_num_std = st.sidebar.number_input('BB Num Std Dev', min_value=1.0, value=2.0)
#rsi_window = st.sidebar.number_input('RSI Window', min_value=1, value=14)
#rsi_overbought = st.sidebar.number_input('RSI Overbought', min_value=1, max_value=100, value=70)
#rsi_oversold = st.sidebar.number_input('RSI Oversold', min_value=1, max_value=100, value=30)

# Only show relevant parameter boxes
short_window = long_window = bb_window = bb_num_std = rsi_window = rsi_overbought = rsi_oversold = None
if strategy_choice == 'SMA Crossover':
    short_window = st.sidebar.number_input('Short MA Window', min_value=1, value=20)
    long_window = st.sidebar.number_input('Long MA Window', min_value=2, value=50)
elif strategy_choice == 'Bollinger Bands':
    bb_window = st.sidebar.number_input('BB Window', min_value=1, value=20)
    bb_num_std = st.sidebar.number_input('BB Num Std Dev', min_value=1.0, value=2.0)
elif strategy_choice == 'RSI':
    rsi_window = st.sidebar.number_input('RSI Window', min_value=1, value=14)
    rsi_overbought = st.sidebar.number_input('RSI Overbought', min_value=1, max_value=100, value=70)
    rsi_oversold = st.sidebar.number_input('RSI Oversold', min_value=1, max_value=100, value=30)

if st.sidebar.button('Fetch & Analyze'):
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        st.error('No data found for the selected symbol and date range.')
    else:
        fig, ax = plt.subplots(figsize=(12,6))
        if strategy_choice == 'SMA Crossover':
            data = calculate_moving_averages(data, short_window, long_window)
            signals = sma_crossover_signals(data, short_window, long_window)
            ax.plot(data.index, data['Close'], label='Close Price')
            ax.plot(data.index, data[f'SMA_{short_window}'], label=f'SMA {short_window}')
            ax.plot(data.index, data[f'SMA_{long_window}'], label=f'SMA {long_window}')
            # Plot buy/sell signals with custom colors
            # Long Call (Buy): dark green, Short Call (Sell): light green, Long Put (Buy): dark red, Short Put (Sell): light red
            # For all strategies, Buy = Long Call (dark green), Sell = Long Put (dark red)
            ax.plot(signals['Buy'].index, signals['Buy']['Close'], '^', markersize=10, color='#006400', label='Long Call (Buy)')  # dark green
            ax.plot(signals['Sell'].index, signals['Sell']['Close'], 'v', markersize=10, color='#8B0000', label='Long Put (Sell)')  # dark red
            ax.legend()
            st.pyplot(fig)
            # Basic performance
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
            wins = 0
            total = 0
            for buy_time in buy_indices:
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
        elif strategy_choice == 'Bollinger Bands':
            from strategy import bollinger_bands_signals
            signals = bollinger_bands_signals(data, window=bb_window, num_std=bb_num_std)
            ax.plot(data.index, data['Close'], label='Close Price')
            ax.plot(data.index, signals['Upper'], label='Upper Band', linestyle='--', color='orange')
            ax.plot(data.index, signals['Lower'], label='Lower Band', linestyle='--', color='orange')
            ax.plot(data.index, signals['MA'], label=f'BB MA {bb_window}', linestyle=':', color='blue')
            # Plot buy/sell signals with custom colors
            # For all strategies, Buy = Long Call (dark green), Sell = Long Put (dark red)
            ax.plot(signals['Buy'].index, signals['Buy']['Close'], '^', markersize=10, color='#006400', label='Long Call (Buy)')  # dark green
            ax.plot(signals['Sell'].index, signals['Sell']['Close'], 'v', markersize=10, color='#8B0000', label='Long Put (Sell)')  # dark red
            ax.legend()
            st.pyplot(fig)
            # Basic performance for BB
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
        elif strategy_choice == 'RSI':
            from strategy import rsi_signals
            signals = rsi_signals(data, window=rsi_window, overbought=rsi_overbought, oversold=rsi_oversold)
            ax.plot(data.index, data['Close'], label='Close Price')
            ax2 = ax.twinx()
            ax2.plot(data.index, signals['RSI'], label='RSI', color='purple', alpha=0.5)
            ax2.axhline(rsi_overbought, color='red', linestyle='--', alpha=0.5, label='Overbought')
            ax2.axhline(rsi_oversold, color='green', linestyle='--', alpha=0.5, label='Oversold')
            # Plot buy/sell signals with custom colors
            # For all strategies, Buy = Long Call (dark green), Sell = Long Put (dark red)
            ax.plot(signals['Buy'].index, signals['Buy']['Close'], '^', markersize=10, color='#006400', label='Long Call (Buy)')  # dark green
            ax.plot(signals['Sell'].index, signals['Sell']['Close'], 'v', markersize=10, color='#8B0000', label='Long Put (Sell)')  # dark red
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')
            st.pyplot(fig)
            # Basic performance for RSI
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
