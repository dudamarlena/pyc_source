# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\strategy\positionControlStrategy.py
# Compiled at: 2019-08-30 20:58:11
# Size of source mod 2**32: 2145 bytes
"""
20190822 09：45

lw 李文写的仓位控制模块
"""
from pyalgotrade.broker import gmEnum
from pyalgotrade import commonHelpBylw
import datetime

class intraDayPositionControl:

    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.intraOpenCountLimit = kwargs.get('intraOpenCountLimit', None)
        self.intraOpenLongCountLimit = kwargs.get('intraOpenLongCountLimit', None)
        self.intraOpenShortCountLimit = kwargs.get('intraOpenShortCountLimit', None)
        self._intraDayPositionControl__intradaycLongOpenCount = 0
        self._intraDayPositionControl__intradaycShortOpenCount = 0
        self._intraDayPositionControl__intradayOpenCount = 0

    def onbar(self, lastBarDT, currBarDT):
        if commonHelpBylw.isCrossDay(self.symbol, lastBarDT, currBarDT):
            self._intraDayPositionControl__intradaycLongOpenCount = 0
            self._intraDayPositionControl__intradaycShortOpenCount = 0
            self._intraDayPositionControl__intradayOpenCount = 0
        longOpenLimitFlag = self._intraDayPositionControl__intradaycLongOpenCount < self.intraOpenLongCountLimit
        shortOpenLimitFlag = self._intraDayPositionControl__intradaycShortOpenCount < self.intraOpenShortCountLimit
        return (
         longOpenLimitFlag, shortOpenLimitFlag)

    def onTradeReport(self, execrpt):
        if execrpt['position_effect'] == gmEnum.PositionEffect_Open:
            if execrpt['side'] == gmEnum.OrderSide_Buy:
                self._intraDayPositionControl__intradaycLongOpenCount = self._intraDayPositionControl__intradaycLongOpenCount + 1
                self._intraDayPositionControl__intradayOpenCount = self._intraDayPositionControl__intradayOpenCount + 1
        if execrpt['position_effect'] == gmEnum.PositionEffect_Open:
            if execrpt['side'] == gmEnum.OrderSide_Sell:
                self._intraDayPositionControl__intradaycShortOpenCount = self._intraDayPositionControl__intradaycShortOpenCount + 1
                self._intraDayPositionControl__intradayOpenCount = self._intraDayPositionControl__intradayOpenCount + 1
        i = 1