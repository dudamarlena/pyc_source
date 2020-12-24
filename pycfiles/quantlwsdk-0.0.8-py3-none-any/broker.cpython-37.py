# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\broker.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 4714 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import broker
from pyalgotrade.broker import backtesting
from pyalgotrade.bitstamp import common
from pyalgotrade.bitstamp import livebroker
LiveBroker = livebroker.LiveBroker

class BacktestingBroker(backtesting.Broker):
    MIN_TRADE_USD = 5

    def __init__(self, cash, barFeed, fee=0.0025):
        commission = backtesting.TradePercentage(fee)
        super(BacktestingBroker, self).__init__(cash, barFeed, commission)

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def submitOrder(self, order):
        if order.isInitial():
            order.setAllOrNone(False)
            order.setGoodTillCanceled(True)
        return super(BacktestingBroker, self).submitOrder(order)

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        raise Exception('Market orders are not supported')

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        if instrument != common.btc_symbol:
            raise Exception('Only BTC instrument is supported')
        if action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        else:
            if action == broker.Order.Action.SELL_SHORT:
                action = broker.Order.Action.SELL
            elif limitPrice * quantity < BacktestingBroker.MIN_TRADE_USD:
                raise Exception('Trade must be >= %s' % BacktestingBroker.MIN_TRADE_USD)
            elif action == broker.Order.Action.BUY:
                fee = self.getCommission().calculate(None, limitPrice, quantity)
                cashRequired = limitPrice * quantity + fee
                if cashRequired > self.getCash(False):
                    raise Exception('Not enough cash')
            elif action == broker.Order.Action.SELL:
                if quantity > self.getShares(common.btc_symbol):
                    raise Exception('Not enough %s' % common.btc_symbol)
            else:
                raise Exception('Only BUY/SELL orders are supported')
            return super(BacktestingBroker, self).createLimitOrder(action, instrument, limitPrice, quantity)

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        raise Exception('Stop orders are not supported')

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        raise Exception('Stop limit orders are not supported')


class PaperTradingBroker(BacktestingBroker):
    __doc__ = 'A Bitstamp paper trading broker.\n\n    :param cash: The initial amount of cash.\n    :type cash: int/float.\n    :param barFeed: The bar feed that will provide the bars.\n    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`\n    :param fee: The fee percentage for each order. Defaults to 0.5%.\n    :type fee: float.\n\n    .. note::\n        * Only limit orders are supported.\n        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.\n        * BUY_TO_COVER orders are mapped to BUY orders.\n        * SELL_SHORT orders are mapped to SELL orders.\n    '