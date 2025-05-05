import yfinance as yf
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Stock, PriceHistory
import pandas as pd


def fetch_and_store_stock_data(symbol: str = None):
    """
    Fetch historical stock data using yfinance and store it in the database.
    If symbol is None, fetches for all symbols in the Stock table.
    """
    symbols = [symbol.upper()] if symbol else [s.symbol for s in Stock.query.all()]

    for sym in symbols:
        print(f"Fetching data for: {sym}")
        ticker = yf.Ticker(sym)

        last_price = PriceHistory.query.filter_by(symbol=sym).order_by(PriceHistory.date.desc()).first()
        start_date = (last_price.date if last_price else None)


        try:
            if start_date:
                hist = ticker.history(start=start_date + pd.Timedelta(days=1))  # Avoid duplicate
            else:
                hist = ticker.history(period="1y")
        except Exception as e:
            print(f"Failed to fetch data for {sym}: {e}")
            continue

        if hist.empty:
            print(f"No data returned for symbol: {sym}")
            continue


        stock = Stock.query.filter_by(symbol=sym).first()
        if not stock:
            stock = Stock(symbol=sym, name=sym)
            db.session.add(stock)
            db.session.commit()

        existing_dates = {
            p.date for p in PriceHistory.query.filter_by(symbol=sym).all()
        }

        new_prices = []
        for date, row in hist.iterrows():
            date_obj = date.to_pydatetime().date()
            if date_obj in existing_dates:
                continue

            price = PriceHistory(
                stock_id=stock.id,
                symbol=sym,
                date=date_obj,
                open=row["Open"],
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                volume=int(row["Volume"]) if not pd.isna(row["Volume"]) else None
            )
            new_prices.append(price)

        if new_prices:
            db.session.bulk_save_objects(new_prices)
            try:
                db.session.commit()
                print(f"Saved {len(new_prices)} new records for {sym}")
            except IntegrityError:
                db.session.rollback()
                print(f"Integrity error while saving price history for {sym}")
