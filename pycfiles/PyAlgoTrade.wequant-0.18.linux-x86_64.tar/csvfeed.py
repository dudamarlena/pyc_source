# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/feed/csvfeed.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, datetime
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from pyalgotrade.feed import memfeed

class RowParser(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parseRow(self, csvRowDict):
        raise NotImplementedError()

    @abc.abstractmethod
    def getFieldNames(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getDelimiter(self):
        raise NotImplementedError()


class RowFilter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def includeRow(self, dateTime, values):
        raise NotImplementedError()


class DateRangeFilter(RowFilter):

    def __init__(self, fromDate=None, toDate=None):
        self.__fromDate = fromDate
        self.__toDate = toDate

    def includeRow(self, dateTime, values):
        if self.__toDate and dateTime > self.__toDate:
            return False
        if self.__fromDate and dateTime < self.__fromDate:
            return False
        return True


class BaseFeed(memfeed.MemFeed):

    def __init__(self, rowParser, maxLen=None):
        super(BaseFeed, self).__init__(maxLen)
        self.__rowParser = rowParser
        self.__rowFilter = None
        return

    def setRowFilter(self, rowFilter):
        self.__rowFilter = rowFilter

    def addValuesFromCSV(self, path):
        values = []
        reader = csvutils.FastDictReader(open(path, 'r'), fieldnames=self.__rowParser.getFieldNames(), delimiter=self.__rowParser.getDelimiter())
        for row in reader:
            dateTime, rowValues = self.__rowParser.parseRow(row)
            if dateTime is not None and (self.__rowFilter is None or self.__rowFilter.includeRow(dateTime, rowValues)):
                values.append((dateTime, rowValues))

        self.addValues(values)
        return


class BasicRowParser(RowParser):

    def __init__(self, dateTimeColumn, dateTimeFormat, converter, delimiter=',', timezone=None):
        self.__dateTimeColumn = dateTimeColumn
        self.__dateTimeFormat = dateTimeFormat
        self.__converter = converter
        self.__delimiter = delimiter
        self.__timezone = timezone
        self.__timeDelta = None
        return

    def parseRow(self, csvRowDict):
        dateTime = datetime.datetime.strptime(csvRowDict[self.__dateTimeColumn], self.__dateTimeFormat)
        if self.__timezone is not None:
            if self.__timeDelta is not None:
                dateTime += self.__timeDelta
            dateTime = dt.localize(dateTime, self.__timezone)
        values = {}
        for key, value in csvRowDict.items():
            if key != self.__dateTimeColumn:
                values[key] = self.__converter(key, value)

        return (
         dateTime, values)

    def getFieldNames(self):
        return

    def getDelimiter(self):
        return self.__delimiter

    def setTimeDelta(self, timeDelta):
        self.__timeDelta = timeDelta


def float_or_string(column, value):
    return csvutils.float_or_string(value)


class Feed(BaseFeed):
    """A feed that loads values from CSV formatted files.

    :param dateTimeColumn: The name of the column that has the datetime information.
    :type dateTimeColumn: string.
    :param dateTimeFormat: The datetime format. datetime.datetime.strptime will be used to parse the column.
    :type dateTimeFormat: string.
    :param converter: A function with two parameters (column name and value) used to convert the string
        value to something else. The default coverter will try to convert the value to a float. If that fails
        the original string is returned.
    :type converter: function.
    :param delimiter: The string used to separate values.
    :type delimiter: string.
    :param timezone: The timezone to use to localize datetimes. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that each :class:`pyalgotrade.dataseries.DataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dateTimeColumn, dateTimeFormat, converter=None, delimiter=',', timezone=None, maxLen=None):
        if converter is None:
            converter = float_or_string
        self.__rowParser = BasicRowParser(dateTimeColumn, dateTimeFormat, converter, delimiter, timezone)
        super(Feed, self).__init__(self.__rowParser, maxLen)
        return

    def addValuesFromCSV(self, path):
        """Loads values from a file.

        :param path: The path to the CSV file.
        :type path: string.
        """
        return super(Feed, self).addValuesFromCSV(path)

    def setDateRange(self, fromDateTime, toDateTime):
        self.setRowFilter(DateRangeFilter(fromDateTime, toDateTime))

    def setTimeDelta(self, timeDelta):
        self.__rowParser.setTimeDelta(timeDelta)