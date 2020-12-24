# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\feed\csvfeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 6214 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, datetime, six
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from pyalgotrade.feed import memfeed

@six.add_metaclass(abc.ABCMeta)
class RowParser(object):

    @abc.abstractmethod
    def parseRow(self, csvRowDict):
        raise NotImplementedError()

    @abc.abstractmethod
    def getFieldNames(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getDelimiter(self):
        raise NotImplementedError()


@six.add_metaclass(abc.ABCMeta)
class RowFilter(object):

    @abc.abstractmethod
    def includeRow(self, dateTime, values):
        raise NotImplementedError()


class DateRangeFilter(RowFilter):

    def __init__(self, fromDate=None, toDate=None):
        self._DateRangeFilter__fromDate = fromDate
        self._DateRangeFilter__toDate = toDate

    def includeRow(self, dateTime, values):
        if self._DateRangeFilter__toDate:
            if dateTime > self._DateRangeFilter__toDate:
                return False
        if self._DateRangeFilter__fromDate:
            if dateTime < self._DateRangeFilter__fromDate:
                return False
        return True


class BaseFeed(memfeed.MemFeed):

    def __init__(self, rowParser, maxLen=None):
        super(BaseFeed, self).__init__(maxLen)
        self._BaseFeed__rowParser = rowParser
        self._BaseFeed__rowFilter = None

    def setRowFilter(self, rowFilter):
        self._BaseFeed__rowFilter = rowFilter

    def addValuesFromCSV(self, path):
        values = []
        reader = csvutils.FastDictReader((open(path, 'r')), fieldnames=(self._BaseFeed__rowParser.getFieldNames()), delimiter=(self._BaseFeed__rowParser.getDelimiter()))
        for row in reader:
            dateTime, rowValues = self._BaseFeed__rowParser.parseRow(row)
            if not dateTime is not None or self._BaseFeed__rowFilter is None or self._BaseFeed__rowFilter.includeRow(dateTime, rowValues):
                values.append((dateTime, rowValues))

        self.addValues(values)


class BasicRowParser(RowParser):

    def __init__(self, dateTimeColumn, dateTimeFormat, converter, delimiter=',', timezone=None):
        self._BasicRowParser__dateTimeColumn = dateTimeColumn
        self._BasicRowParser__dateTimeFormat = dateTimeFormat
        self._BasicRowParser__converter = converter
        self._BasicRowParser__delimiter = delimiter
        self._BasicRowParser__timezone = timezone
        self._BasicRowParser__timeDelta = None

    def parseRow(self, csvRowDict):
        dateTime = datetime.datetime.strptime(csvRowDict[self._BasicRowParser__dateTimeColumn], self._BasicRowParser__dateTimeFormat)
        if self._BasicRowParser__timezone is not None:
            if self._BasicRowParser__timeDelta is not None:
                dateTime += self._BasicRowParser__timeDelta
            dateTime = dt.localize(dateTime, self._BasicRowParser__timezone)
        values = {}
        for key, value in csvRowDict.items():
            if key != self._BasicRowParser__dateTimeColumn:
                values[key] = self._BasicRowParser__converter(key, value)

        return (
         dateTime, values)

    def getFieldNames(self):
        pass

    def getDelimiter(self):
        return self._BasicRowParser__delimiter

    def setTimeDelta(self, timeDelta):
        self._BasicRowParser__timeDelta = timeDelta


def float_or_string(column, value):
    return csvutils.float_or_string(value)


class Feed(BaseFeed):
    __doc__ = 'A feed that loads values from CSV formatted files.\n\n    :param dateTimeColumn: The name of the column that has the datetime information.\n    :type dateTimeColumn: string.\n    :param dateTimeFormat: The datetime format. datetime.datetime.strptime will be used to parse the column.\n    :type dateTimeFormat: string.\n    :param converter: A function with two parameters (column name and value) used to convert the string\n        value to something else. The default coverter will try to convert the value to a float. If that fails\n        the original string is returned.\n    :type converter: function.\n    :param delimiter: The string used to separate values.\n    :type delimiter: string.\n    :param timezone: The timezone to use to localize datetimes. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that each :class:`pyalgotrade.dataseries.DataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dateTimeColumn, dateTimeFormat, converter=None, delimiter=',', timezone=None, maxLen=None):
        if converter is None:
            converter = float_or_string
        self._Feed__rowParser = BasicRowParser(dateTimeColumn, dateTimeFormat, converter, delimiter, timezone)
        super(Feed, self).__init__(self._Feed__rowParser, maxLen)

    def addValuesFromCSV(self, path):
        return super(Feed, self).addValuesFromCSV(path)

    def setDateRange(self, fromDateTime, toDateTime):
        self.setRowFilter(DateRangeFilter(fromDateTime, toDateTime))

    def setTimeDelta(self, timeDelta):
        self._Feed__rowParser.setTimeDelta(timeDelta)