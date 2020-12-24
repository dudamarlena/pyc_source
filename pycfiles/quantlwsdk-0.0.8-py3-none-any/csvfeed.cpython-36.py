# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\barfeed\csvfeed.py
# Compiled at: 2019-06-05 03:25:53
# Size of source mod 2**32: 10354 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import datetime, pytz, six
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from pyalgotrade.barfeed import membf
from pyalgotrade import bar

class RowParser(object):

    def parseBar(self, csvRowDict):
        raise NotImplementedError()

    def getFieldNames(self):
        raise NotImplementedError()

    def getDelimiter(self):
        raise NotImplementedError()


class BarFilter(object):

    def includeBar(self, bar_):
        raise NotImplementedError()


class DateRangeFilter(BarFilter):

    def __init__(self, fromDate=None, toDate=None):
        self._DateRangeFilter__fromDate = fromDate
        self._DateRangeFilter__toDate = toDate

    def includeBar(self, bar_):
        if self._DateRangeFilter__toDate:
            if bar_.getDateTime() > self._DateRangeFilter__toDate:
                return False
        if self._DateRangeFilter__fromDate:
            if bar_.getDateTime() < self._DateRangeFilter__fromDate:
                return False
        return True


class USEquitiesRTH(DateRangeFilter):
    timezone = pytz.timezone('US/Eastern')

    def __init__(self, fromDate=None, toDate=None):
        super(USEquitiesRTH, self).__init__(fromDate, toDate)
        self._USEquitiesRTH__fromTime = datetime.time(9, 30, 0)
        self._USEquitiesRTH__toTime = datetime.time(16, 0, 0)

    def includeBar(self, bar_):
        ret = super(USEquitiesRTH, self).includeBar(bar_)
        if ret:
            barDay = bar_.getDateTime().weekday()
            if barDay > 4:
                return False
            barTime = dt.localize(bar_.getDateTime(), USEquitiesRTH.timezone).time()
            if barTime < self._USEquitiesRTH__fromTime:
                return False
            if barTime > self._USEquitiesRTH__toTime:
                return False
        return ret


class BarFeed(membf.BarFeed):
    __doc__ = 'Base class for CSV file based :class:`pyalgotrade.barfeed.BarFeed`.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

    def __init__(self, frequency, maxLen=None):
        super(BarFeed, self).__init__(frequency, maxLen)
        self._BarFeed__barFilter = None
        self._BarFeed__dailyTime = datetime.time(0, 0, 0)

    def getDailyBarTime(self):
        return self._BarFeed__dailyTime

    def setDailyBarTime(self, time):
        self._BarFeed__dailyTime = time

    def getBarFilter(self):
        return self._BarFeed__barFilter

    def setBarFilter(self, barFilter):
        self._BarFeed__barFilter = barFilter

    def addBarsFromCSV(self, instrument, path, rowParser, skipMalformedBars=False):

        def parse_bar_skip_malformed(row):
            ret = None
            try:
                ret = rowParser.parseBar(row)
            except Exception:
                pass

            return ret

        if skipMalformedBars:
            parse_bar = parse_bar_skip_malformed
        else:
            parse_bar = rowParser.parseBar
        loadedBars = []
        reader = csvutils.FastDictReader((open(path, 'r')), fieldnames=(rowParser.getFieldNames()), delimiter=(rowParser.getDelimiter()))
        for row in reader:
            bar_ = parse_bar(row)
            if bar_ is not None and (self._BarFeed__barFilter is None or self._BarFeed__barFilter.includeBar(bar_)):
                loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)


class GenericRowParser(RowParser):

    def __init__(self, columnNames, dateTimeFormat, dailyBarTime, frequency, timezone, barClass=bar.BasicBar):
        self._GenericRowParser__dateTimeFormat = dateTimeFormat
        self._GenericRowParser__dailyBarTime = dailyBarTime
        self._GenericRowParser__frequency = frequency
        self._GenericRowParser__timezone = timezone
        self._GenericRowParser__haveAdjClose = False
        self._GenericRowParser__barClass = barClass
        self._GenericRowParser__dateTimeColName = columnNames['datetime']
        self._GenericRowParser__openColName = columnNames['open']
        self._GenericRowParser__highColName = columnNames['high']
        self._GenericRowParser__lowColName = columnNames['low']
        self._GenericRowParser__closeColName = columnNames['close']
        self._GenericRowParser__volumeColName = columnNames['volume']
        self._GenericRowParser__adjCloseColName = columnNames['adj_close']
        self._GenericRowParser__columnNames = columnNames

    def _parseDate(self, dateString):
        ret = datetime.datetime.strptime(dateString, self._GenericRowParser__dateTimeFormat)
        if self._GenericRowParser__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self._GenericRowParser__dailyBarTime)
        if self._GenericRowParser__timezone:
            ret = dt.localize(ret, self._GenericRowParser__timezone)
        return ret

    def barsHaveAdjClose(self):
        return self._GenericRowParser__haveAdjClose

    def getFieldNames(self):
        pass

    def getDelimiter(self):
        return ','

    def parseBar(self, csvRowDict):
        dateTime = self._parseDate(csvRowDict[self._GenericRowParser__dateTimeColName])
        open_ = float(csvRowDict[self._GenericRowParser__openColName])
        high = float(csvRowDict[self._GenericRowParser__highColName])
        low = float(csvRowDict[self._GenericRowParser__lowColName])
        close = float(csvRowDict[self._GenericRowParser__closeColName])
        volume = float(csvRowDict[self._GenericRowParser__volumeColName])
        adjClose = None
        if self._GenericRowParser__adjCloseColName is not None:
            adjCloseValue = csvRowDict.get(self._GenericRowParser__adjCloseColName, '')
            if len(adjCloseValue) > 0:
                adjClose = float(adjCloseValue)
                self._GenericRowParser__haveAdjClose = True
        extra = {}
        for k, v in six.iteritems(csvRowDict):
            if k not in self._GenericRowParser__columnNames.values():
                extra[k] = csvutils.float_or_string(v)

        return self._GenericRowParser__barClass(dateTime,
          open_, high, low, close, volume, adjClose, (self._GenericRowParser__frequency), extra=extra)


class GenericBarFeed(BarFeed):
    __doc__ = 'A BarFeed that loads bars from CSV files that have the following format:\n    ::\n\n        Date Time,Open,High,Low,Close,Volume,Adj Close\n        2013-01-01 13:59:00,13.51001,13.56,13.51,13.56,273.88014126,13.51001\n\n    :param frequency: The frequency of the bars. Check :class:`pyalgotrade.bar.Frequency`.\n    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        * The CSV file **must** have the column names in the first row.\n        * It is ok if the **Adj Close** column is empty.\n        * When working with multiple instruments:\n\n         * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.\n         * If any of the instruments loaded are in different timezones, then the timezone parameter should be set.\n    '

    def __init__(self, frequency, timezone=None, maxLen=None):
        super(GenericBarFeed, self).__init__(frequency, maxLen)
        self._GenericBarFeed__timezone = timezone
        self._GenericBarFeed__haveAdjClose = False
        self._GenericBarFeed__barClass = bar.BasicBar
        self._GenericBarFeed__dateTimeFormat = '%Y-%m-%d %H:%M:%S'
        self._GenericBarFeed__columnNames = {'datetime':'Date Time', 
         'open':'Open', 
         'high':'High', 
         'low':'Low', 
         'close':'Close', 
         'volume':'Volume', 
         'adj_close':'Adj Close'}
        self.setDailyBarTime(None)

    def barsHaveAdjClose(self):
        return self._GenericBarFeed__haveAdjClose

    def setNoAdjClose(self):
        self._GenericBarFeed__columnNames['adj_close'] = None
        self._GenericBarFeed__haveAdjClose = False

    def setColumnName(self, col, name):
        self._GenericBarFeed__columnNames[col] = name

    def setDateTimeFormat(self, dateTimeFormat):
        """
        Set the format string to use with strptime to parse datetime column.
        """
        self._GenericBarFeed__dateTimeFormat = dateTimeFormat

    def setBarClass(self, barClass):
        self._GenericBarFeed__barClass = barClass

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
            timezone = self._GenericBarFeed__timezone
        rowParser = GenericRowParser(self._GenericBarFeed__columnNames, self._GenericBarFeed__dateTimeFormat, self.getDailyBarTime(), self.getFrequency(), timezone, self._GenericBarFeed__barClass)
        super(GenericBarFeed, self).addBarsFromCSV(instrument, path, rowParser, skipMalformedBars=skipMalformedBars)
        if rowParser.barsHaveAdjClose():
            self._GenericBarFeed__haveAdjClose = True
        elif self._GenericBarFeed__haveAdjClose:
            raise Exception("Previous bars had adjusted close and these ones don't have.")