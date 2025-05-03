import pandas as pd

def compute_ema(close_prices: pd.Series, window: int) -> pd.Series:
    return close_prices.ewm(span=window, adjust=False).mean()
