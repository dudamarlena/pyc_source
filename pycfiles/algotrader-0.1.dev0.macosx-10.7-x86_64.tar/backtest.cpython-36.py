# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/backtest.py
# Compiled at: 2018-12-16 03:02:54
# Size of source mod 2**32: 2884 bytes
import pandas as pd

class Backtest:

    def __init__(self, agent, cash, stock=0, logging=False, ticker=None):
        self.agent = agent
        self.cash = cash
        self.stock = stock
        self.logging = logging
        self.ticker = ticker
        if logging:
            if ticker is None:
                raise Exception('Ticker not defined. Unable to log records')
            from arctic import Arctic
            self.store = Arctic('localhost')
            self.store.initialize_library('TransactionLogs')
            self.logstore = self.store['TransactionLogs']

    def getPortfolioVal(self, price):
        return int(self.stock * price + self.cash)

    def buy_all(self, price):
        if self.cash > price:
            self.stock += self.cash // price
            self.cash -= self.cash // price * price

    def sell_all(self, price):
        if self.stock > 0:
            self.cash += self.stock * price
            self.stock = 0

    def run(self, data, dates=None):
        results = []
        sell_count = 0
        buy_val = 0
        win_count = 0
        for i in range(len(data)):
            action = None
            if dates is not None:
                action = self.agent.step(data[i], dates[i])
            else:
                action = self.agent.step(data[i])
            if action == 1:
                buy_val = data[i]
                self.buy_all(data[i])
            else:
                if action == -1:
                    sell_count += 1
                    self.sell_all(data[i])
                    if data[i] > buy_val:
                        win_count += 1
            val = self.getPortfolioVal(data[i])
            if self.logging:
                action_type = None
                if action == 0:
                    action_type = 'Hold'
                if action == 1:
                    action_type = 'Buy'
                if action == -1:
                    action_type = 'Sell'
                d = {'Timestep':i,  'Portfolio Value':val,  'Action':action_type}
                df = pd.DataFrame(data=d, index=[i])
                self.logstore.append((self.ticker), df, upsert=True)
            results.append(val)

        if self.stock > 0:
            sell_count += 1
            if buy_val > 0:
                if data[(len(data) - 1)] > buy_val:
                    win_count += 1
        return results