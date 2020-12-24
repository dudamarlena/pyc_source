# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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