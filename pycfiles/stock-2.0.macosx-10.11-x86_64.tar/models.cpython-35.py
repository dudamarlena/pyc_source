# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/models.py
# Compiled at: 2017-02-12 07:19:54
# Size of source mod 2**32: 2435 bytes
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from . import config as C
engine = sql.create_engine(C.DATABASE_URL, **C.CREATE_ENGINE)
Base = declarative_base(bind=engine)
Session = sql.orm.sessionmaker(bind=engine)

def create_all():
    Base.metadata.create_all()


def drop_all():
    Base.metadata.drop_all()


class QuandlCode(Base):
    __tablename__ = 'quandl_code'
    code = sql.Column(sql.String(64), primary_key=True)
    database_code = sql.Column(sql.String(64), nullable=True)

    @property
    def quandl_code(self):
        return self.code

    def __repr__(self):
        return 'QuandlCode({code})'.format(**self.__dict__)


class Price(Base):
    __tablename__ = 'price'
    __table_args__ = (sql.UniqueConstraint('date', 'quandl_code'),)
    high = sql.Column(sql.Float, nullable=True)
    low = sql.Column(sql.Float, nullable=True)
    open = sql.Column(sql.Float, nullable=True)
    close = sql.Column(sql.Float, nullable=True)
    date = sql.Column(sql.Date, nullable=False, index=True)
    quandl_code = sql.Column(sql.String(64), nullable=False, index=True)
    volume = sql.Column(sql.Integer, nullable=True)
    id = sql.Column(sql.Integer, primary_key=True)

    @sql.orm.validates('quandl_code')
    def validate_quandl_code(self, _key, val):
        return val.upper()


class CurrentPrice(Base):
    __tablename__ = 'current_price'
    __table_args__ = (sql.UniqueConstraint('datetime', 'quandl_code'),)
    value = sql.Column(sql.Integer, nullable=False)
    datetime = sql.Column(sql.DateTime, nullable=False, index=True)
    quandl_code = sql.Column(sql.String(64), nullable=False, index=True)
    id = sql.Column(sql.Integer, primary_key=True)