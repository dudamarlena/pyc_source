# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\resamplebase.py
# Compiled at: 2019-06-05 03:26:10
# Size of source mod 2**32: 4521 bytes
import abc, datetime, six
from pyalgotrade.utils import dt
from pyalgotrade import bar

@six.add_metaclass(abc.ABCMeta)
class TimeRange(object):

    @abc.abstractmethod
    def belongs(self, dateTime):
        raise NotImplementedError()

    @abc.abstractmethod
    def getBeginning(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getEnding(self):
        raise NotImplementedError()


class IntraDayRange(TimeRange):

    def __init__(self, dateTime, frequency):
        super(IntraDayRange, self).__init__()
        assert isinstance(frequency, int)
        assert frequency > 1
        assert frequency < bar.Frequency.DAY
        ts = int(dt.datetime_to_timestamp(dateTime))
        slot = int(ts / frequency)
        slotTs = slot * frequency
        self._IntraDayRange__begin = dt.timestamp_to_datetime(slotTs, not dt.datetime_is_naive(dateTime))
        if not dt.datetime_is_naive(dateTime):
            self._IntraDayRange__begin = dt.localize(self._IntraDayRange__begin, dateTime.tzinfo)
        self._IntraDayRange__end = self._IntraDayRange__begin + datetime.timedelta(seconds=frequency)

    def belongs(self, dateTime):
        return dateTime >= self._IntraDayRange__begin and dateTime < self._IntraDayRange__end

    def getBeginning(self):
        return self._IntraDayRange__begin

    def getEnding(self):
        return self._IntraDayRange__end


class DayRange(TimeRange):

    def __init__(self, dateTime):
        super(DayRange, self).__init__()
        self._DayRange__begin = datetime.datetime(dateTime.year, dateTime.month, dateTime.day)
        if not dt.datetime_is_naive(dateTime):
            self._DayRange__begin = dt.localize(self._DayRange__begin, dateTime.tzinfo)
        self._DayRange__end = self._DayRange__begin + datetime.timedelta(days=1)

    def belongs(self, dateTime):
        return dateTime >= self._DayRange__begin and dateTime < self._DayRange__end

    def getBeginning(self):
        return self._DayRange__begin

    def getEnding(self):
        return self._DayRange__end


class MonthRange(TimeRange):

    def __init__(self, dateTime):
        super(MonthRange, self).__init__()
        self._MonthRange__begin = datetime.datetime(dateTime.year, dateTime.month, 1)
        if dateTime.month == 12:
            self._MonthRange__end = datetime.datetime(dateTime.year + 1, 1, 1)
        else:
            self._MonthRange__end = datetime.datetime(dateTime.year, dateTime.month + 1, 1)
        if not dt.datetime_is_naive(dateTime):
            self._MonthRange__begin = dt.localize(self._MonthRange__begin, dateTime.tzinfo)
            self._MonthRange__end = dt.localize(self._MonthRange__end, dateTime.tzinfo)

    def belongs(self, dateTime):
        return dateTime >= self._MonthRange__begin and dateTime < self._MonthRange__end

    def getBeginning(self):
        return self._MonthRange__begin

    def getEnding(self):
        return self._MonthRange__end


def is_valid_frequency(frequency):
    if not isinstance(frequency, int):
        raise AssertionError
    elif not frequency > 1:
        raise AssertionError
    elif frequency < bar.Frequency.DAY:
        ret = True
    else:
        if frequency == bar.Frequency.DAY:
            ret = True
        else:
            if frequency == bar.Frequency.MONTH:
                ret = True
            else:
                ret = False
    return ret


def build_range(dateTime, frequency):
    if not isinstance(frequency, int):
        raise AssertionError
    elif not frequency > 1:
        raise AssertionError
    elif frequency < bar.Frequency.DAY:
        ret = IntraDayRange(dateTime, frequency)
    else:
        if frequency == bar.Frequency.DAY:
            ret = DayRange(dateTime)
        else:
            if frequency == bar.Frequency.MONTH:
                ret = MonthRange(dateTime)
            else:
                raise Exception('Unsupported frequency')
    return ret


@six.add_metaclass(abc.ABCMeta)
class Grouper(object):

    def __init__(self, groupDateTime):
        self._Grouper__groupDateTime = groupDateTime

    def getDateTime(self):
        return self._Grouper__groupDateTime

    @abc.abstractmethod
    def addValue(self, value):
        """Add a value to the group."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getGrouped(self):
        """Return the grouped value."""
        raise NotImplementedError()