# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\stratanalyzer\returns.py
# Compiled at: 2019-06-05 03:26:10
# Size of source mod 2**32: 8809 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import math
from pyalgotrade import stratanalyzer
from pyalgotrade import observer
from pyalgotrade import dataseries

class TimeWeightedReturns(object):

    def __init__(self, initialValue):
        self._TimeWeightedReturns__lastValue = initialValue
        self._TimeWeightedReturns__flows = 0.0
        self._TimeWeightedReturns__lastPeriodRet = 0.0
        self._TimeWeightedReturns__cumRet = 0.0

    def deposit(self, amount):
        self._TimeWeightedReturns__flows += amount

    def withdraw(self, amount):
        self._TimeWeightedReturns__flows -= amount

    def getCurrentValue(self):
        return self._TimeWeightedReturns__lastValue

    def update(self, currentValue):
        if self._TimeWeightedReturns__lastValue:
            retSubperiod = (currentValue - self._TimeWeightedReturns__lastValue - self._TimeWeightedReturns__flows) / float(self._TimeWeightedReturns__lastValue)
        else:
            retSubperiod = 0.0
        self._TimeWeightedReturns__cumRet = (1 + self._TimeWeightedReturns__cumRet) * (1 + retSubperiod) - 1
        self._TimeWeightedReturns__lastPeriodRet = retSubperiod
        self._TimeWeightedReturns__lastValue = currentValue
        self._TimeWeightedReturns__flows = 0.0

    def getLastPeriodReturns(self):
        return self._TimeWeightedReturns__lastPeriodRet

    def getCumulativeReturns(self):
        return self._TimeWeightedReturns__cumRet


class PositionTracker(object):

    def __init__(self, instrumentTraits):
        self._PositionTracker__instrumentTraits = instrumentTraits
        self.reset()

    def reset(self):
        self._PositionTracker__pnl = 0.0
        self._PositionTracker__avgPrice = 0.0
        self._PositionTracker__position = 0.0
        self._PositionTracker__commissions = 0.0
        self._PositionTracker__totalCommited = 0.0

    def getPosition(self):
        return self._PositionTracker__position

    def getAvgPrice(self):
        return self._PositionTracker__avgPrice

    def getCommissions(self):
        return self._PositionTracker__commissions

    def getPnL(self, price=None, includeCommissions=True):
        """
        Return the PnL that would result if closing the position a the given price.
        Note that this will be different if commissions are used when the trade is executed.
        """
        ret = self._PositionTracker__pnl
        if price:
            ret += (price - self._PositionTracker__avgPrice) * self._PositionTracker__position
        if includeCommissions:
            ret -= self._PositionTracker__commissions
        return ret

    def getReturn(self, price=None, includeCommissions=True):
        ret = 0
        pnl = self.getPnL(price=price, includeCommissions=includeCommissions)
        if self._PositionTracker__totalCommited != 0:
            ret = pnl / float(self._PositionTracker__totalCommited)
        return ret

    def __openNewPosition(self, quantity, price):
        self._PositionTracker__avgPrice = price
        self._PositionTracker__position = quantity
        self._PositionTracker__totalCommited = self._PositionTracker__avgPrice * abs(self._PositionTracker__position)

    def __extendCurrentPosition(self, quantity, price):
        newPosition = self._PositionTracker__instrumentTraits.roundQuantity(self._PositionTracker__position + quantity)
        self._PositionTracker__avgPrice = (self._PositionTracker__avgPrice * abs(self._PositionTracker__position) + price * abs(quantity)) / abs(float(newPosition))
        self._PositionTracker__position = newPosition
        self._PositionTracker__totalCommited = self._PositionTracker__avgPrice * abs(self._PositionTracker__position)

    def __reduceCurrentPosition(self, quantity, price):
        assert self._PositionTracker__instrumentTraits.roundQuantity(abs(self._PositionTracker__position) - abs(quantity)) >= 0
        pnl = (price - self._PositionTracker__avgPrice) * quantity * -1
        self._PositionTracker__pnl += pnl
        self._PositionTracker__position = self._PositionTracker__instrumentTraits.roundQuantity(self._PositionTracker__position + quantity)
        if self._PositionTracker__position == 0:
            self._PositionTracker__avgPrice = 0.0

    def update(self, quantity, price, commission):
        if not quantity != 0:
            raise AssertionError('Invalid quantity')
        elif not price > 0:
            raise AssertionError('Invalid price')
        elif not commission >= 0:
            raise AssertionError('Invalid commission')
        else:
            if self._PositionTracker__position == 0:
                self._PositionTracker__openNewPosition(quantity, price)
            else:
                currPosDirection = math.copysign(1, self._PositionTracker__position)
                tradeDirection = math.copysign(1, quantity)
                if currPosDirection == tradeDirection:
                    self._PositionTracker__extendCurrentPosition(quantity, price)
                else:
                    if abs(quantity) <= abs(self._PositionTracker__position):
                        self._PositionTracker__reduceCurrentPosition(quantity, price)
                    else:
                        newPos = self._PositionTracker__position + quantity
                        self._PositionTracker__reduceCurrentPosition(self._PositionTracker__position * -1, price)
                        self._PositionTracker__openNewPosition(newPos, price)
        self._PositionTracker__commissions += commission

    def buy(self, quantity, price, commission=0.0):
        assert quantity > 0, 'Invalid quantity'
        self.update(quantity, price, commission)

    def sell(self, quantity, price, commission=0.0):
        assert quantity > 0, 'Invalid quantity'
        self.update(quantity * -1, price, commission)


class ReturnsAnalyzerBase(stratanalyzer.StrategyAnalyzer):

    def __init__(self):
        super(ReturnsAnalyzerBase, self).__init__()
        self._ReturnsAnalyzerBase__event = observer.Event()
        self._ReturnsAnalyzerBase__portfolioReturns = None

    @classmethod
    def getOrCreateShared(cls, strat):
        name = cls.__name__
        ret = strat.getNamedAnalyzer(name)
        if ret is None:
            ret = ReturnsAnalyzerBase()
            strat.attachAnalyzerEx(ret, name)
        return ret

    def attached(self, strat):
        self._ReturnsAnalyzerBase__portfolioReturns = TimeWeightedReturns(strat.getBroker().getEquity())

    def getEvent(self):
        return self._ReturnsAnalyzerBase__event

    def getNetReturn(self):
        return self._ReturnsAnalyzerBase__portfolioReturns.getLastPeriodReturns()

    def getCumulativeReturn(self):
        return self._ReturnsAnalyzerBase__portfolioReturns.getCumulativeReturns()

    def beforeOnBars(self, strat, bars):
        self._ReturnsAnalyzerBase__portfolioReturns.update(strat.getBroker().getEquity())
        self._ReturnsAnalyzerBase__event.emit(bars.getDateTime(), self)


class Returns(stratanalyzer.StrategyAnalyzer):
    __doc__ = '\n    A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that calculates time-weighted returns for the\n    whole portfolio.\n\n    :param maxLen: The maximum number of values to hold in net and cumulative returs dataseries.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, maxLen=None):
        super(Returns, self).__init__()
        self._Returns__netReturns = dataseries.SequenceDataSeries(maxLen=maxLen)
        self._Returns__cumReturns = dataseries.SequenceDataSeries(maxLen=maxLen)

    def beforeAttach(self, strat):
        analyzer = ReturnsAnalyzerBase.getOrCreateShared(strat)
        analyzer.getEvent().subscribe(self._Returns__onReturns)

    def __onReturns(self, dateTime, returnsAnalyzerBase):
        self._Returns__netReturns.appendWithDateTime(dateTime, returnsAnalyzerBase.getNetReturn())
        self._Returns__cumReturns.appendWithDateTime(dateTime, returnsAnalyzerBase.getCumulativeReturn())

    def getReturns(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the returns for each bar."""
        return self._Returns__netReturns

    def getCumulativeReturns(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the cumulative returns for each bar."""
        return self._Returns__cumReturns