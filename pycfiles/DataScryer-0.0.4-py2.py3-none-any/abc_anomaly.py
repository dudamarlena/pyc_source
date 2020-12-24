# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\methods\abc_anomaly.py
# Compiled at: 2016-09-05 05:45:42
from abc import ABCMeta, abstractmethod

class AnomalyMethod:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_anomaly(self, options, lookback_range, lookback_data):
        raise NotImplementedError()