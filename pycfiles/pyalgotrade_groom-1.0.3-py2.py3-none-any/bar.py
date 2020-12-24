# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/bar.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import abc

class Frequency(object):
    """Enum like class for bar frequencies. Valid values are:

    * **Frequency.TRADE**: The bar represents a single trade.
    * **Frequency.SECOND**: The bar summarizes the trading activity during 1 second.
    * **Frequency.MINUTE**: The bar summarizes the trading activity during 1 minute.
    * **Frequency.HOUR**: The bar summarizes the trading activity during 1 hour.
    * **Frequency.DAY**: The bar summarizes the trading activity during 1 day.
    * **Frequency.WEEK**: The bar summarizes the trading activity during 1 week.
    * **Frequency.MONTH**: The bar summarizes the trading activity during 1 month.
    """
    TRADE = -1
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2678400


class Bar(object):
    """A Bar is a summary of the trading activity for a security in a given period.

    .. note::
        This is a base class and should not be used directly.
    """
    __metaclass__ = abc.ABCMeta

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
        elif high < open_:
            raise Exception('high < open on %s' % dateTime)
        elif high < close:
            raise Exception('high < close on %s' % dateTime)
        elif low > open_:
            raise Exception('low > open on %s' % dateTime)
        elif low > close:
            raise Exception('low > close on %s' % dateTime)
        self.__dateTime = dateTime
        self.__open = open_
        self.__close = close
        self.__high = high
        self.__low = low
        self.__volume = volume
        self.__adjClose = adjClose
        self.__frequency = frequency
        self.__useAdjustedValue = False
        self.__extra = extra

    def __setstate__(self, state):
        self.__dateTime, self.__open, self.__close, self.__high, self.__low, self.__volume, self.__adjClose, self.__frequency, self.__useAdjustedValue, self.__extra = state

    def __getstate__(self):
        return (
         self.__dateTime,
         self.__open,
         self.__close,
         self.__high,
         self.__low,
         self.__volume,
         self.__adjClose,
         self.__frequency,
         self.__useAdjustedValue,
         self.__extra)

    def setUseAdjustedValue(self, useAdjusted):
        if useAdjusted and self.__adjClose is None:
            raise Exception('Adjusted close is not available')
        self.__useAdjustedValue = useAdjusted
        return

    def getUseAdjValue(self):
        return self.__useAdjustedValue

    def getDateTime(self):
        return self.__dateTime

    def getOpen(self, adjusted=False):
        if adjusted:
            if self.__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self.__adjClose * self.__open / float(self.__close)
        else:
            return self.__open
            return

    def getHigh(self, adjusted=False):
        if adjusted:
            if self.__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self.__adjClose * self.__high / float(self.__close)
        else:
            return self.__high
            return

    def getLow(self, adjusted=False):
        if adjusted:
            if self.__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self.__adjClose * self.__low / float(self.__close)
        else:
            return self.__low
            return

    def getClose(self, adjusted=False):
        if adjusted:
            if self.__adjClose is None:
                raise Exception('Adjusted close is missing')
            return self.__adjClose
        else:
            return self.__close
            return

    def getVolume(self):
        return self.__volume

    def getAdjClose(self):
        return self.__adjClose

    def getFrequency(self):
        return self.__frequency

    def getPrice(self):
        if self.__useAdjustedValue:
            return self.__adjClose
        else:
            return self.__close

    def getExtraColumns(self):
        return self.__extra


class Bars(object):
    """A group of :class:`Bar` objects.

    :param barDict: A map of instrument to :class:`Bar` objects.
    :type barDict: map.

    .. note::
        All bars must have the same datetime.
    """

    def __init__(self, barDict):
        if len(barDict) == 0:
            raise Exception('No bars supplied')
        firstDateTime = None
        firstInstrument = None
        for instrument, currentBar in barDict.iteritems():
            if firstDateTime is None:
                firstDateTime = currentBar.getDateTime()
                firstInstrument = instrument
            elif currentBar.getDateTime() != firstDateTime:
                raise Exception('Bar data times are not in sync. %s %s != %s %s' % (
                 instrument,
                 currentBar.getDateTime(),
                 firstInstrument,
                 firstDateTime))

        self.__barDict = barDict
        self.__dateTime = firstDateTime
        return

    def __getitem__(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument.
        If the instrument is not found an exception is raised."""
        return self.__barDict[instrument]

    def __contains__(self, instrument):
        """Returns True if a :class:`pyalgotrade.bar.Bar` for the given instrument is available."""
        return instrument in self.__barDict

    def items(self):
        return self.__barDict.items()

    def keys(self):
        return self.__barDict.keys()

    def getInstruments(self):
        """Returns the instrument symbols."""
        return self.__barDict.keys()

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` for this set of bars."""
        return self.__dateTime

    def getBar(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument or None if the instrument is not found."""
        return self.__barDict.get(instrument, None)