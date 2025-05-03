import pandas as pd
from app.extensions import db
from app.models.price_history import PriceHistory

def get_price_history_df(symbol: str) -> pd.DataFrame:
    """
    Fetch price history data from the database for the given stock symbol
    and return it as a pandas DataFrame.

    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """
    records = (
        db.session.query(PriceHistory)
        .filter(PriceHistory.symbol == symbol)
        .order_by(PriceHistory.date.asc())
        .all()
    )

    if not records:
        return pd.DataFrame()

    data = [{
        'date': record.date,
        'open': record.open,
        'high': record.high,
        'low': record.low,
        'close': record.close,
        'volume': record.volume
    } for record in records]

    return pd.DataFrame(data)
