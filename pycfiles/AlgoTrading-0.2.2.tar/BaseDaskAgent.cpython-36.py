# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/dask-agents/BaseDaskAgent.py
# Compiled at: 2018-12-14 06:55:47
# Size of source mod 2**32: 601 bytes
from collections import deque

class BaseDaskAgent:

    def __init__(self, cash, window_size):
        self.cash = cash
        self.stock = 0
        self.memory = deque(maxlen=window_size)

    def deep_reset(self, cash, stock, stock_price, ticker):
        self.cash = cash
        self.stock = stock
        self.portfolio_val = self.cash + self.stock * self.stock_price
        self.ticker = ticker
        self.memory = deque(maxlen=1000)

    def reset_memory(self):
        self.memory = deque(maxlen=1000)

    def getPortfolioVal(self, price):
        return int(self.stock * price + self.cash)