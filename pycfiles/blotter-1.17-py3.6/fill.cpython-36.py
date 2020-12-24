# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blotter/fill.py
# Compiled at: 2019-07-16 12:01:56
# Size of source mod 2**32: 3834 bytes
import random, datetime as dt
from .directions import DIRECTIONS
from .log import Logger, LOGGING_ENABLED

class _Fill:

    def __init__(self, orderid, ticker, pricelevel, orderfilled, **kwargs):
        self.OrderID = orderid
        self.ClOrderID = orderid
        self.ExecID = random.randint(0, 1000000)
        self.ExchangeTicker = ticker
        self.PriceLevel = float(pricelevel)
        self.OrderFilled = float(orderfilled)
        self.TransactionTime = dt.datetime.now()
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def headers(self):
        return '|'.join([a for a in dir(self) if a[0].isupper()])


class Fill:

    def __init__(self, fill):
        self.OrderID = fill.OrderID
        self.ClOrderID = fill.ClOrderID
        self.ExecID = fill.ExecID
        self.PriceLevel = fill.PriceLevel
        self.OrderFilled = fill.OrderFilled
        self.ExchangeTicker = fill.ExchangeTicker
        self.TransactionTime = fill.TransactionTime
        self.Booked = False
        self.BookedAt = None
        self.BookedPartial = False
        self.BookedPartialAt = None
        self.OpenQuantity = self.OrderFilled
        self.Offsets = []
        self.UnrealPnl = 0
        self.RealPnl = 0
        self.logger = Logger(self.__class__.__name__)

    @staticmethod
    def create_from_attrs(*args, **kwargs):
        return Fill(_Fill(*args, **kwargs))

    @property
    def headers(self):
        return '|'.join([a for a in dir(self) if a[0].isupper()])

    @property
    def TotalPnl(self):
        return self.UnrealPnl + self.RealPnl

    @property
    def Direction(self):
        if not self.OrderFilled:
            raise ValueError(f"Received {__class__.__name__} with 0 quantity")
        if self.OrderFilled > 0:
            return DIRECTIONS.LONG
        else:
            return DIRECTIONS.SHORT

    def __repr__(self):
        direction = 'BUY' if self.Direction.name == DIRECTIONS.LONG.name else 'SELL'
        return f">{__class__.__name__.upper()}|" + f"#{self.OrderID}|" + f"{direction}|" + f"{self.OpenQuantity}/{self.OrderFilled}|" + f"{self.ExchangeTicker}|" + f"{self.PriceLevel}|" + f"{round(self.TotalPnl, 2)}|" + f"{self.TransactionTime}|"

    def book(self, pnl, offset):
        if self.OpenQuantity == offset.OpenQuantity:
            self._book(pnl, offset)
            offset._book(pnl, self)
        else:
            if abs(self.OpenQuantity) - abs(offset.OpenQuantity) < 0:
                offset._book_partial(pnl, self)
                self._book(pnl, offset)
            else:
                self._book_partial(pnl, offset)
                offset._book(pnl, self)

    def _book_partial(self, pnl, offset):
        self.Offsets.append(offset)
        self.BookedPartial = True
        self.BookedPartialAt = dt.datetime.now()
        if abs(offset.OpenQuantity) > abs(self.OpenQuantity):
            if LOGGING_ENABLED:
                self.logger.warn('Warning: Partial Booking OVERFLOW')
            self.OpenQuantity = 0
        else:
            self.OpenQuantity += offset.OpenQuantity
        self.RealPnl += pnl
        if self.OpenQuantity == 0:
            if LOGGING_ENABLED:
                self.logger.warn('Warning: Partial Booking OpenQuantity Reset ')
            self.Booked = True
        if LOGGING_ENABLED:
            self.logger.debug(f"\tBOOKED PARTIAL {self}")

    def _book(self, pnl, offset):
        self.Offsets.append(offset)
        self.Booked = True
        self.BookedAt = self.BookedPartial = True
        self.BookedPartialAt = dt.datetime.now()
        self.OpenQuantity = 0
        self.RealPnl += pnl
        offset.RealPnl = 0
        if LOGGING_ENABLED:
            self.logger.debug(f"\tBOOKED {self}")