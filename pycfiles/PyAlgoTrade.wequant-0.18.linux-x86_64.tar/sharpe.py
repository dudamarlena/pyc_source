# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/stratanalyzer/sharpe.py
# Compiled at: 2016-11-29 01:45:48
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
    """A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that calculates
    Sharpe ratio for the whole portfolio.

    :param useDailyReturns: True if daily returns should be used instead of the returns for each bar.
    :type useDailyReturns: boolean.
    """

    def __init__(self, useDailyReturns=True):
        super(SharpeRatio, self).__init__()
        self.__useDailyReturns = useDailyReturns
        self.__returns = []
        self.__firstDateTime = None
        self.__lastDateTime = None
        self.__currentDate = None
        return

    def getReturns(self):
        return self.__returns

    def beforeAttach(self, strat):
        analyzer = returns.ReturnsAnalyzerBase.getOrCreateShared(strat)
        analyzer.getEvent().subscribe(self.__onReturns)

    def __onReturns(self, dateTime, returnsAnalyzerBase):
        netReturn = returnsAnalyzerBase.getNetReturn()
        if self.__useDailyReturns:
            if dateTime.date() == self.__currentDate:
                self.__returns[-1] = (1 + self.__returns[(-1)]) * (1 + netReturn) - 1
            else:
                self.__currentDate = dateTime.date()
                self.__returns.append(netReturn)
        else:
            self.__returns.append(netReturn)
            if self.__firstDateTime is None:
                self.__firstDateTime = dateTime
            self.__lastDateTime = dateTime
        return

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
        if self.__useDailyReturns:
            ret = sharpe_ratio(self.__returns, riskFreeRate, 252, annualized)
        else:
            ret = sharpe_ratio_2(self.__returns, riskFreeRate, self.__firstDateTime, self.__lastDateTime, annualized)
        return ret