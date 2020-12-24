# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\stratanalyzer\trades.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 8597 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import stratanalyzer
from pyalgotrade import broker
from pyalgotrade.stratanalyzer import returns
import numpy as np

class Trades(stratanalyzer.StrategyAnalyzer):
    __doc__ = "A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that records the profit/loss\n    and returns of every completed trade.\n\n    .. note::\n        This analyzer operates on individual completed trades.\n        For example, lets say you start with a $1000 cash, and then you buy 1 share of XYZ\n        for $10 and later sell it for $20:\n\n            * The trade's profit was $10.\n            * The trade's return is 100%, even though your whole portfolio went from $1000 to $1020, a 2% return.\n    "

    def __init__(self):
        super(Trades, self).__init__()
        self._Trades__all = []
        self._Trades__profits = []
        self._Trades__losses = []
        self._Trades__allReturns = []
        self._Trades__positiveReturns = []
        self._Trades__negativeReturns = []
        self._Trades__allCommissions = []
        self._Trades__profitableCommissions = []
        self._Trades__unprofitableCommissions = []
        self._Trades__evenCommissions = []
        self._Trades__evenTrades = 0
        self._Trades__posTrackers = {}

    def __updateTrades(self, posTracker):
        price = 0
        if not posTracker.getPosition() == 0:
            raise AssertionError
        else:
            netProfit = posTracker.getPnL(price)
            netReturn = posTracker.getReturn(price)
            if netProfit > 0:
                self._Trades__profits.append(netProfit)
                self._Trades__positiveReturns.append(netReturn)
                self._Trades__profitableCommissions.append(posTracker.getCommissions())
            else:
                if netProfit < 0:
                    self._Trades__losses.append(netProfit)
                    self._Trades__negativeReturns.append(netReturn)
                    self._Trades__unprofitableCommissions.append(posTracker.getCommissions())
                else:
                    self._Trades__evenTrades += 1
                    self._Trades__evenCommissions.append(posTracker.getCommissions())
        self._Trades__all.append(netProfit)
        self._Trades__allReturns.append(netReturn)
        self._Trades__allCommissions.append(posTracker.getCommissions())
        posTracker.reset()

    def __updatePosTracker(self, posTracker, price, commission, quantity):
        currentShares = posTracker.getPosition()
        if currentShares > 0:
            if quantity > 0:
                posTracker.buy(quantity, price, commission)
            else:
                newShares = currentShares + quantity
                if newShares == 0:
                    posTracker.sell(currentShares, price, commission)
                    self._Trades__updateTrades(posTracker)
                else:
                    if newShares > 0:
                        posTracker.sell(quantity * -1, price, commission)
                    else:
                        proportionalCommission = commission * currentShares / float(quantity * -1)
                        posTracker.sell(currentShares, price, proportionalCommission)
                        self._Trades__updateTrades(posTracker)
                        proportionalCommission = commission * newShares / float(quantity)
                        posTracker.sell(newShares * -1, price, proportionalCommission)
        else:
            if currentShares < 0:
                if quantity < 0:
                    posTracker.sell(quantity * -1, price, commission)
                else:
                    newShares = currentShares + quantity
                    if newShares == 0:
                        posTracker.buy(currentShares * -1, price, commission)
                        self._Trades__updateTrades(posTracker)
                    else:
                        if newShares < 0:
                            posTracker.buy(quantity, price, commission)
                        else:
                            proportionalCommission = commission * currentShares * -1 / float(quantity)
                            posTracker.buy(currentShares * -1, price, proportionalCommission)
                            self._Trades__updateTrades(posTracker)
                            proportionalCommission = commission * newShares / float(quantity)
                            posTracker.buy(newShares, price, proportionalCommission)
            else:
                if quantity > 0:
                    posTracker.buy(quantity, price, commission)
                else:
                    posTracker.sell(quantity * -1, price, commission)

    def __onOrderEvent(self, broker_, orderEvent):
        if orderEvent.getEventType() not in (broker.OrderEvent.Type.PARTIALLY_FILLED, broker.OrderEvent.Type.FILLED):
            return
        else:
            order = orderEvent.getOrder()
            try:
                posTracker = self._Trades__posTrackers[order.getInstrument()]
            except KeyError:
                posTracker = returns.PositionTracker(order.getInstrumentTraits())
                self._Trades__posTrackers[order.getInstrument()] = posTracker

            execInfo = orderEvent.getEventInfo()
            price = execInfo.getPrice()
            commission = execInfo.getCommission()
            action = order.getAction()
            if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
                quantity = execInfo.getQuantity()
            else:
                if action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
                    quantity = execInfo.getQuantity() * -1
                else:
                    assert False
        self._Trades__updatePosTracker(posTracker, price, commission, quantity)

    def attached(self, strat):
        strat.getBroker().getOrderUpdatedEvent().subscribe(self._Trades__onOrderEvent)

    def getCount(self):
        """Returns the total number of trades."""
        return len(self._Trades__all)

    def getProfitableCount(self):
        """Returns the number of profitable trades."""
        return len(self._Trades__profits)

    def getUnprofitableCount(self):
        """Returns the number of unprofitable trades."""
        return len(self._Trades__losses)

    def getEvenCount(self):
        """Returns the number of trades whose net profit was 0."""
        return self._Trades__evenTrades

    def getAll(self):
        """Returns a numpy.array with the profits/losses for each trade."""
        return np.asarray(self._Trades__all)

    def getProfits(self):
        """Returns a numpy.array with the profits for each profitable trade."""
        return np.asarray(self._Trades__profits)

    def getLosses(self):
        """Returns a numpy.array with the losses for each unprofitable trade."""
        return np.asarray(self._Trades__losses)

    def getAllReturns(self):
        """Returns a numpy.array with the returns for each trade."""
        return np.asarray(self._Trades__allReturns)

    def getPositiveReturns(self):
        """Returns a numpy.array with the positive returns for each trade."""
        return np.asarray(self._Trades__positiveReturns)

    def getNegativeReturns(self):
        """Returns a numpy.array with the negative returns for each trade."""
        return np.asarray(self._Trades__negativeReturns)

    def getCommissionsForAllTrades(self):
        """Returns a numpy.array with the commissions for each trade."""
        return np.asarray(self._Trades__allCommissions)

    def getCommissionsForProfitableTrades(self):
        """Returns a numpy.array with the commissions for each profitable trade."""
        return np.asarray(self._Trades__profitableCommissions)

    def getCommissionsForUnprofitableTrades(self):
        """Returns a numpy.array with the commissions for each unprofitable trade."""
        return np.asarray(self._Trades__unprofitableCommissions)

    def getCommissionsForEvenTrades(self):
        """Returns a numpy.array with the commissions for each trade whose net profit was 0."""
        return np.asarray(self._Trades__evenCommissions)