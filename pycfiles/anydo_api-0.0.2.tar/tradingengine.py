# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/tribler/Tribler/community/market/core/tradingengine.py
# Compiled at: 2019-05-07 09:06:53


class TradingEngine(object):
    """
    This class implements the trading engine which interacts with the order matching/negotiation middleware.
    It will be invoked when a trade has been negotiated between two parties.
    """

    def __init__(self, matching_community=None):
        self.pending_trades = []
        self.completed_trades = []
        self.matching_community = matching_community

    def trade(self, trade):
        raise NotImplementedError()