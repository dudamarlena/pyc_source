# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\commission.py
# Compiled at: 2017-08-04 21:59:28
# Size of source mod 2**32: 1651 bytes
"""
@author: sharon
"""
DEFAULT_PER_SHARE_COST = 0.0075
DEFAULT_MINIMUM_COST_PER_TRADE = 1.0

class CommissionModel:
    pass


class PerShare(CommissionModel):

    def __init__(self, cost=DEFAULT_PER_SHARE_COST, min_trade_cost=DEFAULT_MINIMUM_COST_PER_TRADE):
        self.cost_per_share = float(cost)
        self.min_trade_cost = min_trade_cost

    def __repr__(self):
        return '{class_name}(cost_per_share={cost_per_share}, min_trade_cost={min_trade_cost})'.format(class_name=(self.__class__.__name__),
          cost_per_share=(self.cost_per_share),
          min_trade_cost=(self.min_trade_cost))


class PerTrade(CommissionModel):

    def __init__(self, cost=DEFAULT_MINIMUM_COST_PER_TRADE):
        """
        Cost parameter is the cost of a trade, regardless of share count.
        $5.00 per trade is fairly typical of discount brokers.
        """
        self.cost = float(cost)


class PerDollar(CommissionModel):

    def __init__(self, cost=0.0015):
        """
        Cost parameter is the cost of a trade per-dollar. 0.0015
        on $1 million means $1,500 commission (=1M * 0.0015)
        """
        self.cost_per_dollar = float(cost)

    def __repr__(self):
        return '{class_name}(cost_per_dollar={cost})'.format(class_name=(self.__class__.__name__),
          cost=(self.cost_per_dollar))