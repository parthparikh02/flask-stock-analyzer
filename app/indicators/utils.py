from app.models.price_history import PriceHistory
from app.models.stock import Stock
import pandas as pd

def get_price_history_df(symbol: str) -> pd.DataFrame:
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return pd.DataFrame()

    prices = PriceHistory.query.filter_by(stock_id=stock.id).order_by(PriceHistory.date).all()
    data = [{
        'date': p.date,
        'close': p.close,
        'open': p.open,
        'high': p.high,
        'low': p.low,
        'volume': p.volume
    } for p in prices]

    return pd.DataFrame(data)
