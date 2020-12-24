# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\bar.py
# Compiled at: 2019-06-05 03:25:52
# Size of source mod 2**32: 9067 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six

class Frequency(object):
    __doc__ = 'Enum like class for bar frequencies. Valid values are:\n\n    * **Frequency.TRADE**: The bar represents a single trade.\n    * **Frequency.SECOND**: The bar summarizes the trading activity during 1 second.\n    * **Frequency.MINUTE**: The bar summarizes the trading activity during 1 minute.\n    * **Frequency.HOUR**: The bar summarizes the trading activity during 1 hour.\n    * **Frequency.DAY**: The bar summarizes the trading activity during 1 day.\n    * **Frequency.WEEK**: The bar summarizes the trading activity during 1 week.\n    * **Frequency.MONTH**: The bar summarizes the trading activity during 1 month.\n    '
    TRADE = -1
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2678400


@six.add_metaclass(abc.ABCMeta)
class Bar(object):
    __doc__ = 'A Bar is a summary of the trading activity for a security in a given period.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

    @abc.abstractmethod
    def setUseAdjustedValue(self, useAdjusted):
        raise NotImplementedError()

    @abc.abstractmethod
    def getUseAdjValue(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getDateTime(self):
        """Returns the :class:`datetime.datetime`."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getOpen(self, adjusted=False):
        """Returns the opening price."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getHigh(self, adjusted=False):
        """Returns the highest price."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getLow(self, adjusted=False):
        """Returns the lowest price."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getClose(self, adjusted=False):
        """Returns the closing price."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getVolume(self):
        """Returns the volume."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getAdjClose(self):
        """Returns the adjusted closing price."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getFrequency(self):
        """The bar's period."""
        raise NotImplementedError()

    def getTypicalPrice(self):
        """Returns the typical price."""
        return (self.getHigh() + self.getLow() + self.getClose()) / 3.0

    @abc.abstractmethod
    def getPrice(self):
        """Returns the closing or adjusted closing price."""
        raise NotImplementedError()

    def getExtraColumns(self):
        return {}


class BasicBar(Bar):
    __slots__ = ('__dateTime', '__open', '__close', '__high', '__low', '__volume',
                 '__adjClose', '__frequency', '__useAdjustedValue', '__extra')

    def __init__(self, dateTime, open_, high, low, close, volume, adjClose, frequency, extra={}):
        if high < low:
            raise Exception('high < low on %s' % dateTime)
        else:
            if high < open_:
                raise Exception('high < open on %s' % dateTime)
            else:
                if high < close:
                    raise Exception('high < close on %s' % dateTime)
                else:
                    if low > open_:
                        raise Exception('low > open on %s' % dateTime)
                    else:
                        if low > close:
                            raise Exception('low > close on %s' % dateTime)
        self._BasicBar__dateTime = dateTime
        self._BasicBar__open = open_
        self._BasicBar__close = close
        self._BasicBar__high = high
        self._BasicBar__low = low
        self._BasicBar__volume = volume
        self._BasicBar__adjClose = adjClose
        self._BasicBar__frequency = frequency
        self._BasicBar__useAdjustedValue = False
        self._BasicBar__extra = extra

    def __setstate__(self, state):
        self._BasicBar__dateTime, self._BasicBar__open, self._BasicBar__close, self._BasicBar__high, self._BasicBar__low, self._BasicBar__volume, self._BasicBar__adjClose, self._BasicBar__frequency, self._BasicBar__useAdjustedValue, self._BasicBar__extra = state

    def __getstate__(self):
        return (
         self._BasicBar__dateTime,
         self._BasicBar__open,
         self._BasicBar__close,
         self._BasicBar__high,
         self._BasicBar__low,
         self._BasicBar__volume,
         self._BasicBar__adjClose,
         self._BasicBar__frequency,
         self._BasicBar__useAdjustedValue,
         self._BasicBar__extra)

    def setUseAdjustedValue(self, useAdjusted):
        if useAdjusted:
            if self._BasicBar__adjClose is None:
                raise Exception('Adjusted close is not available')
        self._BasicBar__useAdjustedValue = useAdjusted

    def getUseAdjValue(self):
        return self._BasicBar__useAdjustedValue

    def getDateTime(self):
        return self._BasicBar__dateTime

    def getOpen(self, adjusted=False):
        if adjusted:
            if self._BasicBar__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self._BasicBar__adjClose * self._BasicBar__open / float(self._BasicBar__close)
        return self._BasicBar__open

    def getHigh(self, adjusted=False):
        if adjusted:
            if self._BasicBar__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self._BasicBar__adjClose * self._BasicBar__high / float(self._BasicBar__close)
        return self._BasicBar__high

    def getLow(self, adjusted=False):
        if adjusted:
            if self._BasicBar__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self._BasicBar__adjClose * self._BasicBar__low / float(self._BasicBar__close)
        return self._BasicBar__low

    def getClose(self, adjusted=False):
        if adjusted:
            if self._BasicBar__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self._BasicBar__adjClose
        return self._BasicBar__close

    def getVolume(self):
        return self._BasicBar__volume

    def getAdjClose(self):
        return self._BasicBar__adjClose

    def getFrequency(self):
        return self._BasicBar__frequency

    def getPrice(self):
        if self._BasicBar__useAdjustedValue:
            return self._BasicBar__adjClose
        return self._BasicBar__close

    def getExtraColumns(self):
        return self._BasicBar__extra


class Bars(object):
    __doc__ = 'A group of :class:`Bar` objects.\n\n    :param barDict: A map of instrument to :class:`Bar` objects.\n    :type barDict: map.\n\n    .. note::\n        All bars must have the same datetime.\n    '

    def __init__(self, barDict):
        if len(barDict) == 0:
            raise Exception('No bars supplied')
        firstDateTime = None
        firstInstrument = None
        for instrument, currentBar in six.iteritems(barDict):
            if firstDateTime is None:
                firstDateTime = currentBar.getDateTime()
                firstInstrument = instrument

        self._Bars__barDict = barDict
        self._Bars__dateTime = firstDateTime

    def __getitem__(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument.
        If the instrument is not found an exception is raised."""
        return self._Bars__barDict[instrument]

    def __contains__(self, instrument):
        """Returns True if a :class:`pyalgotrade.bar.Bar` for the given instrument is available."""
        return instrument in self._Bars__barDict

    def items(self):
        return list(self._Bars__barDict.items())

    def keys(self):
        return list(self._Bars__barDict.keys())

    def getInstruments(self):
        """Returns the instrument symbols."""
        return list(self._Bars__barDict.keys())

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` for this set of bars."""
        return self._Bars__dateTime

    def getBar(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument or None if the instrument is not found."""
        return self._Bars__barDict.get(instrument, None)