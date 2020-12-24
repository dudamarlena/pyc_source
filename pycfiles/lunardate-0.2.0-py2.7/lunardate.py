# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/lunardate.py
# Compiled at: 2018-10-07 10:59:09
"""
A Chinese Calendar Library in Pure Python
=========================================

Chinese Calendar: http://en.wikipedia.org/wiki/Chinese_calendar

Usage
-----
        >>> LunarDate.fromSolarDate(1976, 10, 1)
        LunarDate(1976, 8, 8, 1)
        >>> LunarDate(1976, 8, 8, 1).toSolarDate()
        datetime.date(1976, 10, 1)
        >>> LunarDate(1976, 8, 8, 1).year
        1976
        >>> LunarDate(1976, 8, 8, 1).month
        8
        >>> LunarDate(1976, 8, 8, 1).day
        8
        >>> LunarDate(1976, 8, 8, 1).isLeapMonth
        True

        >>> today = LunarDate.today()
        >>> type(today).__name__
        'LunarDate'

        >>> # support '+' and '-' between datetime.date and datetime.timedelta
        >>> ld = LunarDate(1976,8,8)
        >>> sd = datetime.date(2008,1,1)
        >>> td = datetime.timedelta(days=10)
        >>> ld-ld
        datetime.timedelta(0)
        >>> (ld-sd).days
        -11444
        >>> ld-td
        LunarDate(1976, 7, 27, 0)
        >>> (sd-ld).days
        11444
        >>> ld+td
        LunarDate(1976, 8, 18, 0)
        >>> td+ld
        LunarDate(1976, 8, 18, 0)
        >>> ld2 = LunarDate.today()
        >>> ld < ld2
        True
        >>> ld <= ld2
        True
        >>> ld > ld2
        False
        >>> ld >= ld2
        False
        >>> ld == ld2
        False
        >>> ld != ld2
        True
        >>> ld == ld
        True
        >>> LunarDate.today() == LunarDate.today()
        True
        >>> before_leap_month = LunarDate.fromSolarDate(2088, 5, 17)
        >>> before_leap_month.year
        2088
        >>> before_leap_month.month
        4
        >>> before_leap_month.day
        27
        >>> before_leap_month.isLeapMonth
        False
        >>> leap_month = LunarDate.fromSolarDate(2088, 6, 17)
        >>> leap_month.year
        2088
        >>> leap_month.month
        4
        >>> leap_month.day
        28
        >>> leap_month.isLeapMonth
        True
        >>> after_leap_month = LunarDate.fromSolarDate(2088, 7, 17)
        >>> after_leap_month.year
        2088
        >>> after_leap_month.month
        5
        >>> after_leap_month.day
        29
        >>> after_leap_month.isLeapMonth
        False

Limits
------

this library can only deal with year from 1900 to 2099 (in chinese calendar).

See also
--------

* lunar: http://packages.qa.debian.org/l/lunar.html,
  A converter written in C, this program is derived from it.
* python-lunar: http://code.google.com/p/liblunar/
  Another library written in C, including a python binding.
"""
import datetime
__version__ = '0.2.0'
__all__ = ['LunarDate']

class LunarDate(object):
    _startDate = datetime.date(1900, 1, 31)

    def __init__(self, year, month, day, isLeapMonth=False):
        self.year = year
        self.month = month
        self.day = day
        self.isLeapMonth = bool(isLeapMonth)

    def __str__(self):
        return 'LunarDate(%d, %d, %d, %d)' % (self.year, self.month, self.day, self.isLeapMonth)

    __repr__ = __str__

    @staticmethod
    def fromSolarDate(year, month, day):
        """
        >>> LunarDate.fromSolarDate(1900, 1, 31)
        LunarDate(1900, 1, 1, 0)
        >>> LunarDate.fromSolarDate(2008, 10, 2)
        LunarDate(2008, 9, 4, 0)
        >>> LunarDate.fromSolarDate(1976, 10, 1)
        LunarDate(1976, 8, 8, 1)
        >>> LunarDate.fromSolarDate(2033, 10, 23)
        LunarDate(2033, 10, 1, 0)
        """
        solarDate = datetime.date(year, month, day)
        offset = (solarDate - LunarDate._startDate).days
        return LunarDate._fromOffset(offset)

    def toSolarDate(self):
        """
        >>> LunarDate(1900, 1, 1).toSolarDate()
        datetime.date(1900, 1, 31)
        >>> LunarDate(2008, 9, 4).toSolarDate()
        datetime.date(2008, 10, 2)
        >>> LunarDate(1976, 8, 8, 1).toSolarDate()
        datetime.date(1976, 10, 1)
        >>> LunarDate(2004, 1, 30).toSolarDate()
        Traceback (most recent call last):
        ...
        ValueError: day out of range
        >>> LunarDate(2004, 13, 1).toSolarDate()
        Traceback (most recent call last):
        ...
        ValueError: month out of range
        >>> LunarDate(2100, 1, 1).toSolarDate()
        Traceback (most recent call last):
        ...
        ValueError: year out of range [1900, 2100)
        >>>
        """

        def _calcDays(yearInfo, month, day, isLeapMonth):
            isLeapMonth = int(isLeapMonth)
            res = 0
            ok = False
            for _month, _days, _isLeapMonth in self._enumMonth(yearInfo):
                if (
                 _month, _isLeapMonth) == (month, isLeapMonth):
                    if 1 <= day <= _days:
                        res += day - 1
                        return res
                    raise ValueError('day out of range')
                res += _days

            raise ValueError('month out of range')

        offset = 0
        start_year = 1900
        end_year = start_year + len(yearInfos)
        if start_year < 1900 or self.year >= end_year:
            raise ValueError(('year out of range [{}, {})').format(start_year, end_year))
        yearIdx = self.year - 1900
        for i in range(yearIdx):
            offset += yearDays[i]

        offset += _calcDays(yearInfos[yearIdx], self.month, self.day, self.isLeapMonth)
        return self._startDate + datetime.timedelta(days=offset)

    def __sub__(self, other):
        if isinstance(other, LunarDate):
            return self.toSolarDate() - other.toSolarDate()
        if isinstance(other, datetime.date):
            return self.toSolarDate() - other
        if isinstance(other, datetime.timedelta):
            res = self.toSolarDate() - other
            return LunarDate.fromSolarDate(res.year, res.month, res.day)
        raise TypeError

    def __rsub__(self, other):
        if isinstance(other, datetime.date):
            return other - self.toSolarDate()

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            res = self.toSolarDate() + other
            return LunarDate.fromSolarDate(res.year, res.month, res.day)
        raise TypeError

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        """
        >>> LunarDate.today() == 5
        False
        """
        if not isinstance(other, LunarDate):
            return False
        return self - other == datetime.timedelta(0)

    def __lt__(self, other):
        """
        >>> LunarDate.today() < LunarDate.today()
        False
        >>> LunarDate.today() < 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        try:
            return self - other < datetime.timedelta(0)
        except TypeError:
            raise TypeError("can't compare LunarDate to %s" % (type(other).__name__,))

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        """
        >>> LunarDate.today() > LunarDate.today()
        False
        >>> LunarDate.today() > 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        return not self <= other

    def __ge__(self, other):
        """
        >>> LunarDate.today() >= LunarDate.today()
        True
        >>> LunarDate.today() >= 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        return not self < other

    @classmethod
    def today(cls):
        res = datetime.date.today()
        return cls.fromSolarDate(res.year, res.month, res.day)

    @staticmethod
    def _enumMonth(yearInfo):
        months = [ (i, 0) for i in range(1, 13) ]
        leapMonth = yearInfo % 16
        if leapMonth == 0:
            pass
        else:
            if leapMonth <= 12:
                months.insert(leapMonth, (leapMonth, 1))
            else:
                raise ValueError('yearInfo %r mod 16 should in [0, 12]' % yearInfo)
            for month, isLeapMonth in months:
                if isLeapMonth:
                    days = (yearInfo >> 16) % 2 + 29
                else:
                    days = (yearInfo >> 16 - month) % 2 + 29
                yield (
                 month, days, isLeapMonth)

    @classmethod
    def _fromOffset(cls, offset):

        def _calcMonthDay(yearInfo, offset):
            for month, days, isLeapMonth in cls._enumMonth(yearInfo):
                if offset < days:
                    break
                offset -= days

            return (
             month, offset + 1, isLeapMonth)

        offset = int(offset)
        for idx, yearDay in enumerate(yearDays):
            if offset < yearDay:
                break
            offset -= yearDay

        year = 1900 + idx
        yearInfo = yearInfos[idx]
        month, day, isLeapMonth = _calcMonthDay(yearInfo, offset)
        return LunarDate(year, month, day, isLeapMonth)


yearInfos = [
 19416,
 19168, 42352, 21717, 53856, 55632,
 91476, 22176, 39632, 21970, 19168,
 42422, 42192, 53840, 119381, 46400,
 54944, 44450, 38320, 84343, 18800,
 42160, 46261, 27216, 27968, 109396,
 11104, 38256, 21234, 18800, 25958,
 54432, 59984, 28309, 23248, 11104,
 100067, 37600, 116951, 51536, 54432,
 120998, 46416, 22176, 107956, 9680,
 37584, 53938, 43344, 46423, 27808,
 46416, 86869, 19872, 42448, 83315,
 21200, 43432, 59728, 27296, 44710,
 43856, 19296, 43748, 42352, 21088,
 62051, 55632, 23383, 22176, 38608,
 19925, 19152, 42192, 54484, 53840,
 54616, 46400, 46496, 103846, 38320,
 18864, 43380, 42160, 45690, 27216,
 27968, 44870, 43872, 38256, 19189,
 18800, 25776, 29859, 59984, 27480,
 23232, 43872, 38613, 37600, 51552,
 55636, 54432, 55888, 30034, 22176,
 43959, 9680, 37584, 51893, 43344,
 46240, 47780, 44368, 21977, 19360,
 42416, 86390, 21168, 43312, 31060,
 27296, 44368, 23378, 19296, 42726,
 42208, 53856, 60005, 54576, 23200,
 30371, 38608, 19195, 19152, 42192,
 118966, 53840, 54560, 56645, 46496,
 22224, 21938, 18864, 42359, 42160,
 43600, 111189, 27936, 44448, 84835,
 37744, 18936, 18800, 25776, 92326,
 59984, 27296, 108228, 43744, 37600,
 53987, 51552, 54615, 54432, 55888,
 23893, 22176, 42704, 21972, 21200,
 43448, 43344, 46240, 46758, 44368,
 21920, 43940, 42416, 21168, 45683,
 26928, 29495, 27296, 44368, 84821,
 19296, 42352, 21732, 53600, 59752,
 54560, 55968, 92838, 22224, 19168,
 43476, 41680, 53584, 62034]

def yearInfo2yearDay(yearInfo):
    """calculate the days in a lunar year from the lunar year's info

    >>> yearInfo2yearDay(0) # no leap month, and every month has 29 days.
    348
    >>> yearInfo2yearDay(1) # 1 leap month, and every month has 29 days.
    377
    >>> yearInfo2yearDay((2**12-1)*16) # no leap month, and every month has 30 days.
    360
    >>> yearInfo2yearDay((2**13-1)*16+1) # 1 leap month, and every month has 30 days.
    390
    >>> # 1 leap month, and every normal month has 30 days, and leap month has 29 days.
    >>> yearInfo2yearDay((2**12-1)*16+1)
    389
    """
    yearInfo = int(yearInfo)
    res = 348
    leap = False
    if yearInfo % 16 != 0:
        leap = True
        res += 29
    yearInfo //= 16
    for i in range(12 + leap):
        if yearInfo % 2 == 1:
            res += 1
        yearInfo //= 2

    return res


yearDays = [ yearInfo2yearDay(x) for x in yearInfos ]

def day2LunarDate(offset):
    offset = int(offset)
    res = LunarDate()
    for idx, yearDay in enumerate(yearDays):
        if offset < yearDay:
            break
        offset -= yearDay

    res.year = 1900 + idx


if __name__ == '__main__':
    import doctest
    failure_count, test_count = doctest.testmod()
    if failure_count > 0:
        import sys
        sys.exit(1)