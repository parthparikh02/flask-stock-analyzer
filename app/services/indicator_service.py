import pandas as pd
from app.indicators.rsi import compute_rsi
from app.indicators.macd import compute_macd
from app.indicators.ema import compute_ema
from app.indicators.sma import compute_sma
from app.utils.data_loader import get_price_history_df  # helper to load data

def calculate_indicators(symbol: str, indicators: dict) -> dict:
    """
    Compute requested indicators for a stock symbol.

    Args:
        symbol (str): Stock symbol
        indicators (dict): Dictionary like {'rsi': True, 'macd': True, 'sma': [20, 50], 'ema': [12, 26]}

    Returns:
        dict: Computed indicator values in {'x': [...], 'y': [...]} format
    """
    df = get_price_history_df(symbol.upper())
    if df.empty or 'close' not in df.columns:
        return {"error": "No price data found for symbol"}

    # Ensure the index is datetime for plotting
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        if 'date' in df.columns:
            df.set_index(pd.to_datetime(df['date']), inplace=True)
        else:
            return {"error": "Date column missing or index not datetime"}

    dates = df.index.strftime("%Y-%m-%d").tolist()
    result = {"x": dates}

    if indicators.get('rsi'):
        rsi_series = compute_rsi(df['close']).fillna("")
        result['rsi'] = {"y": rsi_series.tolist()}

    if indicators.get('macd'):
        macd_line, signal_line, hist = compute_macd(df['close'])
        result['macd'] = {
            "macd_line": {"y": macd_line.fillna("").tolist()},
            "signal_line": {"y": signal_line.fillna("").tolist()},
            "histogram": {"y": hist.fillna("").tolist()},
        }

    if sma_periods := indicators.get('sma'):
        result['sma'] = {}
        for period in sma_periods:
            sma_series = compute_sma(df['close'], period).fillna("")
            result['sma'][str(period)] = {"y": sma_series.tolist()}

    if ema_periods := indicators.get('ema'):
        result['ema'] = {}
        for period in ema_periods:
            ema_series = compute_ema(df['close'], period).fillna("")
            result['ema'][str(period)] = {"y": ema_series.tolist()}

    return result
