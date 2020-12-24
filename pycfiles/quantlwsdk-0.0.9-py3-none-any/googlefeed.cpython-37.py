# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\barfeed\googlefeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5739 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
.. moduleauthor:: Maciej Żok <maciek.zok@gmail.com>
"""
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.barfeed import common
from pyalgotrade.utils import dt
from pyalgotrade import bar
import datetime

def parse_date(date):
    month_abbr = {'Jan':1, 
     'Feb':2,  'Mar':3,  'Apr':4,  'May':5, 
     'Jun':6,  'Jul':7,  'Aug':8,  'Sep':9, 
     'Oct':10,  'Nov':11,  'Dec':12}
    date = date.split('-')
    year = int(date[2]) + 2000
    if year > datetime.datetime.today().year:
        year -= 100
    month = int(month_abbr[date[1]])
    day = int(date[0])
    ret = datetime.datetime(year, month, day)
    return ret


class RowParser(csvfeed.RowParser):

    def __init__(self, dailyBarTime, frequency, timezone=None, sanitize=False):
        self._RowParser__dailyBarTime = dailyBarTime
        self._RowParser__frequency = frequency
        self._RowParser__timezone = timezone
        self._RowParser__sanitize = sanitize

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
        adjClose = None
        if self._RowParser__sanitize:
            open_, high, low, close = common.sanitize_ohlc(open_, high, low, close)
        return bar.BasicBar(dateTime, open_, high, low, close, volume, adjClose, self._RowParser__frequency)


class Feed(csvfeed.BarFeed):
    __doc__ = 'A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Google Finance.\n\n    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** is currently supported.\n    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        Google Finance csv files lack timezone information.\n        When working with multiple instruments:\n\n            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.\n            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.\n    '

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if frequency not in [bar.Frequency.DAY]:
            raise Exception('Invalid frequency.')
        super(Feed, self).__init__(frequency, maxLen)
        self._Feed__timezone = timezone
        self._Feed__sanitizeBars = False

    def sanitizeBars(self, sanitize):
        self._Feed__sanitizeBars = sanitize

    def barsHaveAdjClose(self):
        return False

    def addBarsFromCSV(self, instrument, path, timezone=None, skipMalformedBars=False):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the CSV file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        :param skipMalformedBars: True to skip errors while parsing bars.
        :type skipMalformedBars: boolean.
        """
        if timezone is None:
            timezone = self._Feed__timezone
        rowParser = RowParser(self.getDailyBarTime(), self.getFrequency(), timezone, self._Feed__sanitizeBars)
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser, skipMalformedBars=skipMalformedBars)