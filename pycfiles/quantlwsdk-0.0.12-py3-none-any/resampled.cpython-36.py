# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\dataseries\resampled.py
# Compiled at: 2019-06-05 03:26:04
# Size of source mod 2**32: 5914 bytes
import abc, six
from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards
from pyalgotrade import bar
from pyalgotrade import resamplebase

class AggFunGrouper(resamplebase.Grouper):

    def __init__(self, groupDateTime, value, aggfun):
        super(AggFunGrouper, self).__init__(groupDateTime)
        self._AggFunGrouper__values = [value]
        self._AggFunGrouper__aggfun = aggfun

    def addValue(self, value):
        self._AggFunGrouper__values.append(value)

    def getGrouped(self):
        return self._AggFunGrouper__aggfun(self._AggFunGrouper__values)


class BarGrouper(resamplebase.Grouper):

    def __init__(self, groupDateTime, bar_, frequency):
        super(BarGrouper, self).__init__(groupDateTime)
        self._BarGrouper__open = bar_.getOpen()
        self._BarGrouper__high = bar_.getHigh()
        self._BarGrouper__low = bar_.getLow()
        self._BarGrouper__close = bar_.getClose()
        self._BarGrouper__volume = bar_.getVolume()
        self._BarGrouper__adjClose = bar_.getAdjClose()
        self._BarGrouper__useAdjValue = bar_.getUseAdjValue()
        self._BarGrouper__frequency = frequency

    def addValue(self, value):
        self._BarGrouper__high = max(self._BarGrouper__high, value.getHigh())
        self._BarGrouper__low = min(self._BarGrouper__low, value.getLow())
        self._BarGrouper__close = value.getClose()
        self._BarGrouper__adjClose = value.getAdjClose()
        self._BarGrouper__volume += value.getVolume()

    def getGrouped(self):
        """Return the grouped value."""
        ret = bar.BasicBar(self.getDateTime(), self._BarGrouper__open, self._BarGrouper__high, self._BarGrouper__low, self._BarGrouper__close, self._BarGrouper__volume, self._BarGrouper__adjClose, self._BarGrouper__frequency)
        ret.setUseAdjustedValue(self._BarGrouper__useAdjValue)
        return ret


@six.add_metaclass(abc.ABCMeta)
class DSResampler(object):

    def initDSResampler(self, dataSeries, frequency):
        if not resamplebase.is_valid_frequency(frequency):
            raise Exception('Unsupported frequency')
        self._DSResampler__frequency = frequency
        self._DSResampler__grouper = None
        self._DSResampler__range = None
        dataSeries.getNewValueEvent().subscribe(self._DSResampler__onNewValue)

    @abc.abstractmethod
    def buildGrouper(self, range_, value, frequency):
        raise NotImplementedError()

    def __onNewValue(self, dataSeries, dateTime, value):
        if self._DSResampler__range is None:
            self._DSResampler__range = resamplebase.build_range(dateTime, self._DSResampler__frequency)
            self._DSResampler__grouper = self.buildGrouper(self._DSResampler__range, value, self._DSResampler__frequency)
        else:
            if self._DSResampler__range.belongs(dateTime):
                self._DSResampler__grouper.addValue(value)
            else:
                self.appendWithDateTime(self._DSResampler__grouper.getDateTime(), self._DSResampler__grouper.getGrouped())
                self._DSResampler__range = resamplebase.build_range(dateTime, self._DSResampler__frequency)
                self._DSResampler__grouper = self.buildGrouper(self._DSResampler__range, value, self._DSResampler__frequency)

    def pushLast(self):
        if self._DSResampler__grouper is not None:
            self.appendWithDateTime(self._DSResampler__grouper.getDateTime(), self._DSResampler__grouper.getGrouped())
            self._DSResampler__grouper = None
            self._DSResampler__range = None

    def checkNow(self, dateTime):
        if self._DSResampler__range is not None:
            if not self._DSResampler__range.belongs(dateTime):
                self.appendWithDateTime(self._DSResampler__grouper.getDateTime(), self._DSResampler__grouper.getGrouped())
                self._DSResampler__grouper = None
                self._DSResampler__range = None


class ResampledBarDataSeries(bards.BarDataSeries, DSResampler):
    __doc__ = 'A BarDataSeries that will build on top of another, higher frequency, BarDataSeries.\n    Resampling will take place as new values get pushed into the dataseries being resampled.\n\n    :param dataSeries: The DataSeries instance being resampled.\n    :type dataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`\n    :param frequency: The grouping frequency in seconds. Must be > 0.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded\n        from the opposite end.\n    :type maxLen: int.\n\n    .. note::\n        * Supported resampling frequencies are:\n            * Less than bar.Frequency.DAY\n            * bar.Frequency.DAY\n            * bar.Frequency.MONTH\n    '

    def __init__(self, dataSeries, frequency, maxLen=None):
        if not isinstance(dataSeries, bards.BarDataSeries):
            raise Exception('dataSeries must be a dataseries.bards.BarDataSeries instance')
        super(ResampledBarDataSeries, self).__init__(maxLen)
        self.initDSResampler(dataSeries, frequency)

    def checkNow(self, dateTime):
        return super(ResampledBarDataSeries, self).checkNow(dateTime)

    def buildGrouper(self, range_, value, frequency):
        return BarGrouper(range_.getBeginning(), value, frequency)


class ResampledDataSeries(dataseries.SequenceDataSeries, DSResampler):

    def __init__(self, dataSeries, frequency, aggfun, maxLen=None):
        super(ResampledDataSeries, self).__init__(maxLen)
        self.initDSResampler(dataSeries, frequency)
        self._ResampledDataSeries__aggfun = aggfun

    def buildGrouper(self, range_, value, frequency):
        return AggFunGrouper(range_.getBeginning(), value, self._ResampledDataSeries__aggfun)