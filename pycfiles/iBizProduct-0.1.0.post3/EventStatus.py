# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\EventStatus.py
# Compiled at: 2016-04-11 13:55:17
from abc import abstractmethod
from src.Contracts.iBizSpec import iBizSpec

class EventStatus(iBizSpec):

    @property
    def EventStatus(self):
        pass

    @EventStatus.getter
    @abstractmethod
    def getEventStatus(self):
        pass