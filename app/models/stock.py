from app.extensions import db
from app.models.base import BaseModel

class Stock(BaseModel):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"<Stock {self.symbol}>"
