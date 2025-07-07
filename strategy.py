import pandas as pd

def sma_crossover_signals(data: pd.DataFrame, short_window: int, long_window: int):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0
    signals['short_ma'] = data[f'SMA_{short_window}']
    signals['long_ma'] = data[f'SMA_{long_window}']
    signals['signal'][short_window:] = (
        signals['short_ma'][short_window:] > signals['long_ma'][short_window:]
    ).astype(int)
    signals['positions'] = signals['signal'].diff()
    # Buy/Sell points
    buy = data[signals['positions'] == 1]
    sell = data[signals['positions'] == -1]
    return {'Buy': buy, 'Sell': sell}
