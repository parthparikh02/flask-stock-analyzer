import yfinance as yf
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Stock, PriceHistory
import pandas as pd
def fetch_and_store_stock_data(symbol: str):
    """
    Fetch historical stock data using yfinance and store it in the database.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1y")  # Adjust as needed

    if hist.empty:
        raise Exception(f"No data returned for symbol: {symbol}")

    # Find or create stock
    stock = Stock.query.filter_by(symbol=symbol.upper()).first()
    if not stock:
        stock = Stock(symbol=symbol.upper(), name=symbol.upper())
        db.session.add(stock)
        db.session.commit()

    existing_dates = {
        p.date for p in PriceHistory.query.filter_by(symbol=symbol.upper()).all()
    }

    new_prices = []
    for date, row in hist.iterrows():
        date_obj = date.to_pydatetime().date()
        if date_obj in existing_dates:
            continue  # Skip already stored dates

        price = PriceHistory(
            stock_id=stock.id,
            symbol=symbol.upper(),
            date=date_obj,
            open=row["Open"],
            high=row["High"],
            low=row["Low"],
            close=row["Close"],
            volume=int(row["Volume"]) if not pd.isna(row["Volume"]) else None
        )
        new_prices.append(price)

    db.session.bulk_save_objects(new_prices)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception("Database integrity error while saving price history.")
