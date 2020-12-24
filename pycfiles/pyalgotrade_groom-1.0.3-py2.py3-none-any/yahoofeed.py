# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/barfeed/yahoofeed.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
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
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__sanitize = sanitize
        self.__barClass = barClass

    def __parseDate(self, dateString):
        ret = parse_date(dateString)
        if self.__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self.__dailyBarTime)
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def getFieldNames(self):
        return

    def getDelimiter(self):
        return ','

    def parseBar(self, csvRowDict):
        dateTime = self.__parseDate(csvRowDict['Date'])
        close = float(csvRowDict['Close'])
        open_ = float(csvRowDict['Open'])
        high = float(csvRowDict['High'])
        low = float(csvRowDict['Low'])
        volume = float(csvRowDict['Volume'])
        adjClose = float(csvRowDict['Adj Close'])
        if self.__sanitize:
            open_, high, low, close = common.sanitize_ohlc(open_, high, low, close)
        return self.__barClass(dateTime, open_, high, low, close, volume, adjClose, self.__frequency)


class Feed(csvfeed.BarFeed):
    """A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Yahoo! Finance.

    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        Yahoo! Finance csv files lack timezone information.
        When working with multiple instruments:

            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.
    """

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if isinstance(timezone, int):
            raise Exception('timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.')
        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception('Invalid frequency.')
        super(Feed, self).__init__(frequency, maxLen)
        self.__timezone = timezone
        self.__sanitizeBars = False
        self.__barClass = bar.BasicBar

    def setBarClass(self, barClass):
        self.__barClass = barClass

    def sanitizeBars(self, sanitize):
        self.__sanitizeBars = sanitize

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
            timezone = self.__timezone
        rowParser = RowParser(self.getDailyBarTime(), self.getFrequency(), timezone, self.__sanitizeBars, self.__barClass)
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser)
        return