# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\barfeed\ninjatraderfeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5543 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pyalgotrade.barfeed
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar
from pyalgotrade.utils import dt
import pytz, datetime

def parse_datetime(dateTime):
    year = int(dateTime[0:4])
    month = int(dateTime[4:6])
    day = int(dateTime[6:8])
    hour = int(dateTime[9:11])
    minute = int(dateTime[11:13])
    sec = int(dateTime[13:15])
    return datetime.datetime(year, month, day, hour, minute, sec)


class Frequency(object):
    MINUTE = pyalgotrade.bar.Frequency.MINUTE
    DAILY = pyalgotrade.bar.Frequency.DAY


class RowParser(csvfeed.RowParser):

    def __init__(self, frequency, dailyBarTime, timezone=None):
        self._RowParser__frequency = frequency
        self._RowParser__dailyBarTime = dailyBarTime
        self._RowParser__timezone = timezone

    def __parseDateTime(self, dateTime):
        ret = None
        if self._RowParser__frequency == pyalgotrade.bar.Frequency.MINUTE:
            ret = parse_datetime(dateTime)
        else:
            if self._RowParser__frequency == pyalgotrade.bar.Frequency.DAY:
                ret = datetime.datetime.strptime(dateTime, '%Y%m%d')
                if self._RowParser__dailyBarTime is not None:
                    ret = datetime.datetime.combine(ret, self._RowParser__dailyBarTime)
            elif not False:
                raise AssertionError
        ret = pytz.utc.localize(ret)
        if self._RowParser__timezone:
            ret = dt.localize(ret, self._RowParser__timezone)
        return ret

    def getFieldNames(self):
        return [
         'Date Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    def getDelimiter(self):
        return ';'

    def parseBar(self, csvRowDict):
        dateTime = self._RowParser__parseDateTime(csvRowDict['Date Time'])
        close = float(csvRowDict['Close'])
        open_ = float(csvRowDict['Open'])
        high = float(csvRowDict['High'])
        low = float(csvRowDict['Low'])
        volume = float(csvRowDict['Volume'])
        return bar.BasicBar(dateTime, open_, high, low, close, volume, None, self._RowParser__frequency)


class Feed(csvfeed.BarFeed):
    __doc__ = 'A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files exported from NinjaTrader.\n\n    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.MINUTE** or **pyalgotrade.bar.Frequency.DAY**\n        are supported.\n    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, frequency, timezone=None, maxLen=None):
        if isinstance(timezone, int):
            raise Exception('timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.')
        if frequency not in [bar.Frequency.MINUTE, bar.Frequency.DAY]:
            raise Exception('Invalid frequency.')
        super(Feed, self).__init__(frequency, maxLen)
        self._Feed__timezone = timezone

    def barsHaveAdjClose(self):
        return False

    def addBarsFromCSV(self, instrument, path, timezone=None):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        """
        if isinstance(timezone, int):
            raise Exception('timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.')
        if timezone is None:
            timezone = self._Feed__timezone
        rowParser = RowParser(self.getFrequency(), self.getDailyBarTime(), timezone)
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser)