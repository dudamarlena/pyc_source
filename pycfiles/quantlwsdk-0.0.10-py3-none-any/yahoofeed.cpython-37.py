# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\barfeed\yahoofeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5769 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.barfeed import common
from pyalgotrade.utils import dt
from pyalgotrade import bar
import datetime

def parse_date(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    ret = datetime.datetime(year, month, day)
    return ret


class RowParser(csvfeed.RowParser):

    def __init__(self, dailyBarTime, frequency, timezone=None, sanitize=False, barClass=bar.BasicBar):
        self._RowParser__dailyBarTime = dailyBarTime
        self._RowParser__frequency = frequency
        self._RowParser__timezone = timezone
        self._RowParser__sanitize = sanitize
        self._RowParser__barClass = barClass

    def __parseDate(self, dateString):
        ret = parse_date(dateString)
        if self._RowParser__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self._RowParser__dailyBarTime)
        if self._RowParser__timezone:
            ret = dt.localize(ret, self._RowParser__timezone)
        return ret

    def getFieldNames(self):
        pass

    def getDelimiter(self):
        return ','

    def parseBar(self, csvRowDict):
        dateTime = self._RowParser__parseDate(csvRowDict['Date'])
        close = float(csvRowDict['Close'])
        open_ = float(csvRowDict['Open'])
        high = float(csvRowDict['High'])
        low = float(csvRowDict['Low'])
        volume = float(csvRowDict['Volume'])
        adjClose = float(csvRowDict['Adj Close'])
        if self._RowParser__sanitize:
            open_, high, low, close = common.sanitize_ohlc(open_, high, low, close)
        return self._RowParser__barClass(dateTime, open_, high, low, close, volume, adjClose, self._RowParser__frequency)


class Feed(csvfeed.BarFeed):
    __doc__ = 'A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Yahoo! Finance.\n\n    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**\n        are supported.\n    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        Yahoo! Finance csv files lack timezone information.\n        When working with multiple instruments:\n\n            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.\n            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.\n    '

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if isinstance(timezone, int):
            raise Exception('timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.')
        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception('Invalid frequency.')
        super(Feed, self).__init__(frequency, maxLen)
        self._Feed__timezone = timezone
        self._Feed__sanitizeBars = False
        self._Feed__barClass = bar.BasicBar

    def setBarClass(self, barClass):
        self._Feed__barClass = barClass

    def sanitizeBars(self, sanitize):
        self._Feed__sanitizeBars = sanitize

    def barsHaveAdjClose(self):
        return True

    def addBarsFromCSV(self, instrument, path, timezone=None):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the CSV file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        """
        if isinstance(timezone, int):
            raise Exception('timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.')
        if timezone is None:
            timezone = self._Feed__timezone
        rowParser = RowParser(self.getDailyBarTime(), self.getFrequency(), timezone, self._Feed__sanitizeBars, self._Feed__barClass)
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser)