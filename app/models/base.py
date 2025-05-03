from datetime import datetime
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from dateutil import tz


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=tz.tzlocal()))
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now(tz=tz.tzlocal()), onupdate=datetime.now(tz=tz.tzlocal()))
    deleted_at = db.Column(db.DateTime(timezone=True))

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def first_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
