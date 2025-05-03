from app.extensions import db
from app.models.base import BaseModel

class PriceHistory(BaseModel):
    __tablename__ = 'price_history'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('symbol', 'date', name='uq_symbol_date'),
    )

    def __repr__(self):
        return f"<PriceHistory {self.symbol} - {self.date}>"
