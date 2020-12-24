# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\dataseries\bards.py
# Compiled at: 2019-09-12 05:52:56
# Size of source mod 2**32: 6049 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries
import six

class BarDataSeries(dataseries.SequenceDataSeries):
    __doc__ = 'A DataSeries of :class:`pyalgotrade.bar.Bar` instances.\n\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, maxLen=None):
        super(BarDataSeries, self).__init__(maxLen)
        self._BarDataSeries__openDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__closeDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__highDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__lowDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__volumeDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__adjCloseDS = dataseries.SequenceDataSeries(maxLen)
        self._BarDataSeries__extraDS = {}
        self._BarDataSeries__useAdjustedValues = False

    def __getOrCreateExtraDS(self, name):
        ret = self._BarDataSeries__extraDS.get(name)
        if ret is None:
            ret = dataseries.SequenceDataSeries(self.getMaxLen())
            self._BarDataSeries__extraDS[name] = ret
        return ret

    def setUseAdjustedValues(self, useAdjusted):
        self._BarDataSeries__useAdjustedValues = useAdjusted

    def append(self, bar):
        self.appendWithDateTime(bar.getDateTime(), bar)

    def appendWithDateTime(self, dateTime, bar):
        assert dateTime is not None
        assert bar is not None
        bar.setUseAdjustedValue(self._BarDataSeries__useAdjustedValues)
        self._BarDataSeries__openDS.appendWithDateTime(dateTime, bar.getOpen())
        self._BarDataSeries__closeDS.appendWithDateTime(dateTime, bar.getClose())
        self._BarDataSeries__highDS.appendWithDateTime(dateTime, bar.getHigh())
        self._BarDataSeries__lowDS.appendWithDateTime(dateTime, bar.getLow())
        self._BarDataSeries__volumeDS.appendWithDateTime(dateTime, bar.getVolume())
        self._BarDataSeries__adjCloseDS.appendWithDateTime(dateTime, bar.getAdjClose())
        for name, value in six.iteritems(bar.getExtraColumns()):
            extraDS = self._BarDataSeries__getOrCreateExtraDS(name)
            extraDS.appendWithDateTime(dateTime, value)

        super(BarDataSeries, self).appendWithDateTime(dateTime, bar)

    def getOpenDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the open prices."""
        return self._BarDataSeries__openDS

    def getCloseDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the close prices."""
        return self._BarDataSeries__closeDS

    def getHighDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the high prices."""
        return self._BarDataSeries__highDS

    def getLowDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the low prices."""
        return self._BarDataSeries__lowDS

    def getVolumeDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the volume."""
        return self._BarDataSeries__volumeDS

    def getAdjCloseDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the adjusted close prices."""
        return self._BarDataSeries__adjCloseDS

    def getPriceDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the close or adjusted close prices."""
        if self._BarDataSeries__useAdjustedValues:
            return self._BarDataSeries__adjCloseDS
        return self._BarDataSeries__closeDS

    def getExtraDataSeries(self, name):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` for an extra column."""
        return self._BarDataSeries__getOrCreateExtraDS(name)