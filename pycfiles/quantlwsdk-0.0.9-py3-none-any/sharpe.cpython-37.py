# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\stratanalyzer\sharpe.py
# Compiled at: 2019-06-05 03:26:11
# Size of source mod 2**32: 5391 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import stratanalyzer
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.utils import stats
import math

def days_traded(begin, end):
    delta = end - begin
    ret = delta.days + 1
    return ret


def sharpe_ratio(returns, riskFreeRate, tradingPeriods, annualized=True):
    ret = 0.0
    volatility = stats.stddev(returns, 1)
    if volatility != 0:
        rfPerReturn = riskFreeRate / float(tradingPeriods)
        avgExcessReturns = stats.mean(returns) - rfPerReturn
        ret = avgExcessReturns / volatility
        if annualized:
            ret = ret * math.sqrt(tradingPeriods)
    return ret


def sharpe_ratio_2(returns, riskFreeRate, firstDateTime, lastDateTime, annualized=True):
    ret = 0.0
    volatility = stats.stddev(returns, 1)
    if volatility != 0:
        yearsTraded = days_traded(firstDateTime, lastDateTime) / 365.0
        riskFreeRateForPeriod = riskFreeRate * yearsTraded
        rfPerReturn = riskFreeRateForPeriod / float(len(returns))
        avgExcessReturns = stats.mean(returns) - rfPerReturn
        ret = avgExcessReturns / volatility
        if annualized:
            ret = ret * math.sqrt(len(returns) / yearsTraded)
    return ret


class SharpeRatio(stratanalyzer.StrategyAnalyzer):
    __doc__ = 'A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that calculates\n    Sharpe ratio for the whole portfolio.\n\n    :param useDailyReturns: True if daily returns should be used instead of the returns for each bar.\n    :type useDailyReturns: boolean.\n    '

    def __init__(self, useDailyReturns=True):
        super(SharpeRatio, self).__init__()
        self._SharpeRatio__useDailyReturns = useDailyReturns
        self._SharpeRatio__returns = []
        self._SharpeRatio__firstDateTime = None
        self._SharpeRatio__lastDateTime = None
        self._SharpeRatio__currentDate = None

    def getReturns(self):
        return self._SharpeRatio__returns

    def beforeAttach(self, strat):
        analyzer = returns.ReturnsAnalyzerBase.getOrCreateShared(strat)
        analyzer.getEvent().subscribe(self._SharpeRatio__onReturns)

    def __onReturns(self, dateTime, returnsAnalyzerBase):
        netReturn = returnsAnalyzerBase.getNetReturn()
        if self._SharpeRatio__useDailyReturns:
            if dateTime.date() == self._SharpeRatio__currentDate:
                self._SharpeRatio__returns[-1] = (1 + self._SharpeRatio__returns[(-1)]) * (1 + netReturn) - 1
            else:
                self._SharpeRatio__currentDate = dateTime.date()
                self._SharpeRatio__returns.append(netReturn)
        else:
            self._SharpeRatio__returns.append(netReturn)
            if self._SharpeRatio__firstDateTime is None:
                self._SharpeRatio__firstDateTime = dateTime
            self._SharpeRatio__lastDateTime = dateTime

    def getSharpeRatio(self, riskFreeRate, annualized=True):
        """
        Returns the Sharpe ratio for the strategy execution. If the volatility is 0, 0 is returned.

        :param riskFreeRate: The risk free rate per annum.
        :type riskFreeRate: int/float.
        :param annualized: True if the sharpe ratio should be annualized.
        :type annualized: boolean.
        """
        if not isinstance(annualized, bool):
            raise Exception('tradingPeriods parameter is not supported anymore.')
        elif self._SharpeRatio__useDailyReturns:
            ret = sharpe_ratio(self._SharpeRatio__returns, riskFreeRate, 252, annualized)
        else:
            ret = sharpe_ratio_2(self._SharpeRatio__returns, riskFreeRate, self._SharpeRatio__firstDateTime, self._SharpeRatio__lastDateTime, annualized)
        return ret