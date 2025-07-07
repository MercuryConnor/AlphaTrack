import pandas as pd

def calculate_moving_averages(data: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    data = data.copy()
    data[f'SMA_{short_window}'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data[f'SMA_{long_window}'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data
