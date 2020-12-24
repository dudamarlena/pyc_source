# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: h:\dev\dimensiontabler\DimensionTabler\DefaultConfigs.py
# Compiled at: 2018-03-04 19:20:17
from DimensionTabler import DimTabConfig, DimTab
from DimensionTabler.DimTabEvArgs import *
from DimensionTabler._utils.datetimeUtil import *
import decimal

class ConfDefault(DimTabConfig):

    def __init__(self, tableName):
        super(ConfDefault, self).__init__(tableName)
        self._setDefaults()

    def _setDefaults(self):
        self.Dimensions = [
         DimTabConfig.DimensionConfig(' aktuell', -900, 60),
         DimTabConfig.DimensionConfig('last  1h', -3600, 300),
         DimTabConfig.DimensionConfig('last 12h', -43200, 900),
         DimTabConfig.DimensionConfig('last 24h', -86400, 1800),
         DimTabConfig.DimensionConfig('last  7d', -604800, 3600),
         DimTabConfig.DimensionConfig('last 30d', -2592000, 14400),
         DimTabConfig.DimensionConfig('  before', DimTabConfig.DIMENSION_TIMESEC_PAST, 43200)]
        self.FillGapsWithPreviousResult = True
        self.WaitSecondsBeforeCumulating = 15