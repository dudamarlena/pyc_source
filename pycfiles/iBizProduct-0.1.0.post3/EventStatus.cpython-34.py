# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\EventStatus.py
# Compiled at: 2016-04-11 13:55:17
# Size of source mod 2**32: 262 bytes
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