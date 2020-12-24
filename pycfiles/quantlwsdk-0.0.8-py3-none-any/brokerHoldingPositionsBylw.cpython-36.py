# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\broker\brokerHoldingPositionsBylw.py
# Compiled at: 2019-02-18 08:28:57
# Size of source mod 2**32: 1927 bytes
"""
Created on Wed Dec 19 10:13:59 2018

@author: lw
"""

class HoldingPostions:

    def __init__(self, symbol_, positionSide_, volume_, strategyOrderId_=None):
        self._HoldingPostions__strategyOrderId = strategyOrderId_
        self._HoldingPostions__symbol = symbol_
        self._HoldingPostions__positionSide = positionSide_
        self._HoldingPostions__volume = volume_

    @property
    def symbol(self):
        return self._HoldingPostions__symbol

    @property
    def positionSide(self):
        return self._HoldingPostions__positionSide

    @property
    def volume(self):
        return self._HoldingPostions__volume


class BaseOrderHoldingPostion:

    def __init__(self, symbol_, positionSide_, volume_, cost_, commission=0, strategyOrderId_=None):
        self._BaseOrderHoldingPostion__strategyOrderId = strategyOrderId_
        self._BaseOrderHoldingPostion__symbol = symbol_
        self._BaseOrderHoldingPostion__positionSide = positionSide_
        self._BaseOrderHoldingPostion__volume = volume_
        self._BaseOrderHoldingPostion__cost = cost_
        self._BaseOrderHoldingPostion__commission = commission
        self._BaseOrderHoldingPostion__barsSinceEntry = None

    @property
    def symbol(self):
        return self._BaseOrderHoldingPostion__symbol

    @property
    def positionSide(self):
        return self._BaseOrderHoldingPostion__positionSide

    @property
    def volume(self):
        return self._BaseOrderHoldingPostion__volume

    @volume.setter
    def volume(self, value):
        self._BaseOrderHoldingPostion__volume = value

    @property
    def barsSinceEntry(self):
        return self._BaseOrderHoldingPostion__barsSinceEntry

    @barsSinceEntry.setter
    def barsSinceEntry(self, value):
        if not isinstance(value, int):
            raise ValueError('value must be an integer!')
        self._BaseOrderHoldingPostion__barsSinceEntry = value