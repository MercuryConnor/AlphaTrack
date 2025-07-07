import pandas as pd

def rsi_signals(data: pd.DataFrame, window: int = 14, overbought: float = 70, oversold: float = 30):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
    rs = gain / (loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    signals = pd.DataFrame(index=data.index)
    signals['Buy'] = rsi < oversold
    signals['Sell'] = rsi > overbought
    buy = data[signals['Buy']]
    sell = data[signals['Sell']]
    return {'Buy': buy, 'Sell': sell, 'RSI': rsi}
def bollinger_bands_signals(data: pd.DataFrame, window: int = 20, num_std: float = 2):
    signals = pd.DataFrame(index=data.index)
    rolling_mean = data['Close'].rolling(window=window, min_periods=1).mean()
    rolling_std = data['Close'].rolling(window=window, min_periods=1).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    signals['Buy'] = (data['Close'] < lower_band)
    signals['Sell'] = (data['Close'] > upper_band)
    buy = data[signals['Buy']]
    sell = data[signals['Sell']]
    return {'Buy': buy, 'Sell': sell, 'Upper': upper_band, 'Lower': lower_band, 'MA': rolling_mean}
import pandas as pd

def sma_crossover_signals(data: pd.DataFrame, short_window: int, long_window: int):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    signals['short_ma'] = data[f'SMA_{short_window}']
    signals['long_ma'] = data[f'SMA_{long_window}']
    signals.loc[signals.index[short_window:], 'signal'] = (
        signals['short_ma'][short_window:] > signals['long_ma'][short_window:]
    ).astype(int)
    signals['positions'] = signals['signal'].diff()
    # Buy/Sell points
    buy = data[signals['positions'] == 1]
    sell = data[signals['positions'] == -1]
    return {'Buy': buy, 'Sell': sell}
