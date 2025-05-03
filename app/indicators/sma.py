import pandas as pd

def compute_sma(close_prices: pd.Series, window: int) -> pd.Series:
    return close_prices.rolling(window=window).mean()
