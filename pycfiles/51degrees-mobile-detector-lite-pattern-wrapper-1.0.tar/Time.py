# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\Time.py
# Compiled at: 2005-04-06 18:36:48
__doc__ = '\nDate and time related functionality for use within 4Suite only.\n\nThis module is experimental and may not be staying in 4Suite for long;\napplication developers should avoid forming dependencies on it.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import re, time, calendar, rfc822
_month_days = (
 (
  0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31), (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))

def DayOfYearFromYMD(year, month, day):
    """
    Calculates the Julian day (day of year, between 1 and 366),
    for the given date. This function is accurate for dates back to
    01 Jan 0004 (that's 4 A.D.), when the Julian calendar stabilized.
    """
    days_table = _month_days[calendar.isleap(year)]
    days = 0
    for m in range(1, month):
        days += days_table[m]

    return days + day


def WeekdayFromYMD(year, month, day):
    """
    Calculates the day of week (0=Mon, 6=Sun) for the given date.
    This function is accurate for dates on/after Friday, 15 Oct 1582,
    when the Gregorian reform took effect, although it should be noted
    that some nations didn't adopt the Gregorian calendar until as late
    as the 20th century, so dates that were referenced before then
    would have fallen on a different day of the week, at the time.
    """
    if year == 2001:
        days_from_epoch = 0
    else:
        years = range(2001, year, cmp(year, 2001))
        leap_days = len(filter(calendar.isleap, years))
        days_from_epoch = len(years) * 365 + leap_days
    if year < 2001:
        day_of_year = DayOfYearFromYMD(year, month, day)
        days_from_epoch += 365 + calendar.isleap(year) - day_of_year
        days_from_epoch *= -1
    else:
        days_from_epoch += DayOfYearFromYMD(year, month, day) - 1
    return days_from_epoch % 7


class DT:
    """
    A class that contains the data needed to represent a single point in time
    using many different date and time formats.

    Its constructor requires a UTC (GMT) date and time (year, month (0-11), day
    (0-31), hour (0-23), minute (0-59), second (0-59), millisecond (0-999), plus
    some information to help express this time in local terms: a local time zone
    name, or if that's not available, an hour offset of the local time from GMT
    (-11 to 14, typically), a minute offset of the local time from GMT (0 or 30,
    usually), and an optional flag indicating Daylight Savings Time, to help
    determine the time zone name.
    """
    __module__ = __name__

    def __init__(self, year, month, day, hour, minute, second, milliSecond, daylightSavings, tzName, tzHourOffset, tzMinuteOffset):
        tzMinuteOffset = int(tzMinuteOffset)
        tzHourOffset = int(tzHourOffset)
        milliSecond = float(milliSecond)
        second = int(second)
        minute = int(minute)
        hour = int(hour)
        day = int(day)
        month = int(month)
        year = int(year)
        daylightSavings = not not daylightSavings
        if tzName:
            self._tzName = tzName
        else:
            k = float(tzHourOffset) + float(tzMinuteOffset) / 60.0
            d = self.tzNameTable.get(k)
            if d:
                if daylightSavings:
                    n = d[3]
                    if not n:
                        n = d[2]
                else:
                    n = d[2]
                if not n:
                    n = d[0]
                self._tzName = n
            else:
                self._tzName = ''
        secondShift = 0
        while milliSecond < 0:
            secondShift -= 1
            milliSecond += 1000

        while milliSecond > 999:
            secondShift += 1
            milliSecond -= 1000

        self._milliSecond = milliSecond
        second += secondShift
        minuteShift = 0
        while second < 0:
            minuteShift -= 1
            second += 60

        while second > 59:
            minuteShift += 1
            second -= 60

        self._second = second
        (utcHourShift, self._utcMinute) = self.__normalizeMinute(minute + minuteShift)
        (localHourShift, self._localMinute) = self.__normalizeMinute(minute + minuteShift + tzMinuteOffset)
        (utcDayShift, self._utcHour) = self.__normalizeHour(hour + utcHourShift)
        (localDayShift, self._localHour) = self.__normalizeHour(hour + localHourShift + tzHourOffset)
        (self._utcYear, self._utcMonth, self._utcDay) = self.__normalizeDate(day + utcDayShift, month, year)
        (self._localYear, self._localMonth, self._localDay) = self.__normalizeDate(day + localDayShift, month, year)
        self._tzHourOffset = tzHourOffset
        self._tzMinuteOffset = tzMinuteOffset
        self._utcDayOfYear = DayOfYearFromYMD(self._utcYear, self._utcMonth, self._utcDay)
        self._localDayOfYear = DayOfYearFromYMD(self._localYear, self._localMonth, self._localDay)
        self._utcWeekday = WeekdayFromYMD(self._utcYear, self._utcMonth, self._utcDay)
        self._localWeekday = WeekdayFromYMD(self._localYear, self._localMonth, self._localDay)
        self.stringValue = self.asISO8601DateTime(local=1)

    def asISO8601DateTime(self, local=0):
        """
        Represents this DT object as an ISO 8601 date-time string, using
        UTC time like '2001-01-01T00:00:00Z' if local=0, or local time with
        UTC offset like '2000-12-31T17:00:00-07:00' if local=1.
        """
        return '%s%s' % (self.asISO8601Date(local), self.asISO8601Time(local))

    def asISO8601Date(self, local=0):
        """
        Represents this DT object as an ISO 8601 date-time string, like
        '2001-01-01' if local=0, or '2000-12-31' if local=1. The local date
        may vary from UTC date depending on the time of day that is stored
        in the object.
        """
        if local:
            y = self._localYear
            m = self._localMonth
            d = self._localDay
        else:
            y = self._utcYear
            m = self._utcMonth
            d = self._utcDay
        return '%d-%02d-%02d' % (y, m, d)

    def asISO8601Time(self, local=0):
        """
        Represents this DT object as an ISO 8601 time string, using UTC
        time like 'T00:00:00Z' if local=0, or local time with UTC offset
        like 'T17:00:00-07:00' if local=1
        """
        if local:
            h = self._localHour
            m = self._localMinute
            useTz = 1
        else:
            h = self._utcHour
            m = self._utcMinute
            useTz = 0
        s = self._second
        ms = self._milliSecond * 100
        rt = 'T%02d:%02d:%02d' % (h, m, s)
        if ms:
            t = '%d' % ms
            if len(t) > 3:
                t = t[:3]
            while t and t[(-1)] == '0':
                t = t[:-1]

            rt += ',' + t
        if not useTz or not self._tzHourOffset and not self._tzMinuteOffset:
            rt += 'Z'
        else:
            if self._tzHourOffset < 0:
                sign = '-'
                tzh = -1 * self._tzHourOffset
            else:
                sign = '+'
                tzh = self._tzHourOffset
            rt += '%s%02d:%02d' % (sign, tzh, self._tzMinuteOffset)
        return rt

    def asRFC822DateTime(self, local=0):
        """
        Represents this DT object as an RFC 1123 (which updated RFC 822)
        date string, using UTC time like 'Mon, 01 Jan 2001 00:00:00 GMT' if
        local=0, or local time with time zone indicator or offset like
        'Sun, 31 Dec 2000 17:00:00 MDT' if local=1. Although RFC 822 allows
        the weekday to be optional, it is always included in the returned
        string.
        """
        if local:
            wday = self.abbreviatedWeekdayNameTable[self._localWeekday]
            mon = self.abbreviatedMonthNameTable[self._localMonth]
            day = self._localDay
            year = self._localYear
            hour = self._localHour
            minute = self._localMinute
            if self._tzName and self._tzName in ['GMT', 'EST', 'EDT', 'CST', 'CDT', 'MST', 'MDT', 'PST', 'PDT']:
                tz = self._tzName
            else:
                tz = '%+03d%02d' % (self._tzHourOffset, self._tzMinuteOffset)
        else:
            wday = self.abbreviatedWeekdayNameTable[self._utcWeekday]
            mon = self.abbreviatedMonthNameTable[self._utcMonth]
            day = self._utcDay
            year = self._utcYear
            hour = self._utcHour
            minute = self._utcMinute
            tz = 'GMT'
        return '%s, %02d %s %d %02d:%02d:%02d %s' % (wday, day, mon, year, hour, minute, self._second, tz)

    def asPythonTime(self, local=0):
        """
        Returns the stored date and time as a float indicating the number
        of seconds since the local machine's epoch.
        """
        return time.mktime(self.asPythonTimeTuple(local))

    def asPythonTimeTuple(self, local=0):
        """
        Returns the stored date and time as a Python time tuple, as
        documented in the time module. If the tuple is going to be passed
        to a function that expects the local time, set local=1. The
        Daylight Savings flag is always -1, which means unknown, and may
        or may not have ramifications.
        """
        if local:
            return (self._localYear, self._localMonth, self._localDay, self._localHour, self._localMinute, self._second, self._localWeekday, self._localDayOfYear, -1)
        else:
            return (
             self._utcYear, self._utcMonth, self._utcDay, self._utcHour, self._utcMinute, self._second, self._utcWeekday, self._utcDayOfYear, -1)

    def year(self, local=0):
        """
        Returns the year component of the stored date and time as an int
        like 2001.
        """
        if local:
            return self._localYear
        return self._utcYear

    def month(self, local=0):
        """
        Returns the month component of the stored date and time as an int
        in the range 0-11.
        """
        if local:
            return self._localMonth
        return self._utcMonth

    def monthName(self, local=0):
        """
        Returns the month component of the stored date and time as a
        string like 'January'.
        """
        if local:
            return self.monthNameTable[self._localMonth]
        return self.monthNameTable[self._utcMonth]

    def abbreviatedMonthName(self, local=0):
        """
        Returns the month component of the stored date and time as a
        string like 'Jan'.
        """
        if local:
            return self.abbreviatedMonthNameTable[self._localMonth]
        return self.abbreviatedMonthNameTable[self._utcMonth]

    def day(self, local=0):
        """
        Returns the day component of the stored date and time as an
        integer in the range 1-31.
        """
        if local:
            return self._localDay
        return self._utcDay

    def dayOfYear(self, local=0):
        """
        Returns the day of year component of the stored date and time
        as an int in the range 1-366.
        """
        if local:
            return self._localDayOfYear
        return self._utcDayOfYear

    def dayOfWeek(self, local=0):
        """
        Returns the day of week component of the stored date and time
        as an int in the range 0-6 (0=Monday).
        """
        if local:
            return self._localWeekday
        return self._utcWeekday

    def hour(self, local=0):
        """
        Returns the hour component of the stored date and time as an int
        in the range 0-23.
        """
        if local:
            return self._localHour
        return self._utcHour

    def minute(self, local=0):
        """
        Returns the minute component of the stored date and time as an
        int in the range 0-59.
        """
        if local:
            return self._localMinute
        return self._utcMinute

    def second(self):
        """
        Returns the second component of the stored date and time as an
        int in the range 0-59.
        """
        return self._second

    def milliSecond(self):
        """
        Returns the millisecond component of the stored date and time as
        an int in the range 0-999.
        """
        return self._milliSecond

    def tzName(self):
        """
        Returns the local time's time zone name component of the stored
        date and time as a string like 'MST'.
        """
        return self._tzName

    def tzHourOffset(self):
        """
        Returns the local time's hour offset from GMT component of the
        stored date and time as an int, typically in the range -12 to 14.
        """
        return self._tzHourOffset

    def tzMinuteOffset(self):
        """
        Returns the local time's minute offset from GMT component of the
        stored date and time as an int in the range 0-59.
        """
        return self._tzMinuteOffset

    def __normalizeMinute(self, minute):
        hourShift = 0
        while minute < 0:
            hourShift -= 1
            minute += 60

        while minute > 59:
            hourShift += 1
            minute -= 60

        return (hourShift, minute)

    def __normalizeHour(self, hour):
        dayShift = 0
        while hour < 0:
            dayShift -= 1
            hour += 24

        while hour > 23:
            dayShift += 1
            hour -= 24

        return (dayShift, hour)

    def __normalizeDate(self, day, month, year):
        while month < 1 or month > 12 or day < 1 or day > _month_days[calendar.isleap(year)][month]:
            if month < 1:
                year -= 1
                month += 12
            elif month > 12:
                year += 1
                month -= 12
            elif day < 1:
                month -= 1
                if month == 0:
                    day += 31
                else:
                    day += _month_days[calendar.isleap(year)][month]
            elif day > _month_days[calendar.isleap(year)][month]:
                day -= _month_days[calendar.isleap(year)][month]
                month += 1

        return (
         year, month, day)

    __str__ = asISO8601DateTime

    def __cmp__(self, other):
        if isinstance(other, (str, unicode)):
            return cmp(self.asISO8601DateTime(), other)
        elif isinstance(other, (int, float)):
            return cmp(self.asPythonTime(), other)
        elif not isinstance(other, DT):
            raise TypeError('Cannot Compare DT with %s' % repr(other))
        return cmp(self.asISO8601DateTime(), other.asISO8601DateTime())

    def __hash__(self):
        return id(self)

    abbreviatedMonthNameTable = (
     'ERR', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    monthNameTable = (
     'ERROR', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    weekdayNameTable = (
     'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    abbreviatedWeekdayNameTable = (
     'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    tzNameTable = {0: ('GMT', 'Zulu', 'GMT', 'BST'), 1: ('GMT+1', 'Alpha', 'CET', 'MEST'), 2: ('GMT+2', 'Bravo', 'EET', ''), 3: ('GMT+3', 'Charlie', 'BT', ''), 3.5: ('GMT+3:30', '', '', ''), 4: ('GMT+4', 'Delta', '', ''), 4.5: ('GMT+4:30', '', '', ''), 5: ('GMT+5', 'Echo', '', ''), 5.5: ('GMT+5:30', '', '', ''), 6: ('GMT+6', 'Foxtrot', '', ''), 6.5: ('GMT+6:30', '', '', ''), 7: ('GMT+7', 'Golf', 'WAST', ''), 8: ('GMT+8', 'Hotel', 'CCT', ''), 9: ('GMT+9', 'India', 'JST', ''), 9.5: ('GMT+9:30', '', 'Australia Central Time', ''), 10: ('GMT+10', 'Kilo', 'GST', ''), 10.5: ('GMT+10:30', '', '', ''), 11: ('GMT+11', 'Lima', '', ''), 11.5: ('GMT+11:30', '', '', ''), 12: ('GMT+12', 'Mike', 'NZST', ''), 13: ('GMT+13', '', '', ''), 14: ('GMT+14', '', '', ''), -1: ('GMT-1', 'November', 'WAT', ''), -2: ('GMT-2', 'Oscar', 'AT', ''), -3: ('GMT-3', 'Papa', '', 'ADT'), -3.5: ('GMT-3', '', '', ''), -4: ('GMT-4', 'Quebec', 'AST', 'EDT'), -5: ('GMT-5', 'Romeo', 'EST', 'CDT'), -6: ('GMT-6', 'Sierra', 'CST', 'MDT'), -7: ('GMT-7', 'Tango', 'MST', 'PDT'), -8: ('GMT-8', 'Uniform', 'PST', ''), -8.5: ('GMT-8:30', '', '', 'YDT'), -9: ('GMT-9', 'Victor', 'YST', ''), -9.5: ('GMT-9:30', '', '', 'HDT'), -10: ('GMT-10', 'Whiskey', 'AHST', ''), -11: ('GMT-11', 'XRay', 'NT', ''), -12: ('GMT-11', 'Yankee', 'IDLW', '')}


CENTURY = '(?P<Century>[0-9]{2,2})'
YEAR = '(?P<Year>[0-9]{2,2})'
MONTH = '(?P<Month>[0-9]{2,2})'
DAY = '(?P<Day>[0-9]{2,2})'
BASIC_DATE = '%s?%s%s%s' % (CENTURY, YEAR, MONTH, DAY)
EXTENDED_DATE = '%s?%s-%s-%s' % (CENTURY, YEAR, MONTH, DAY)
YEAR_AND_MONTH_DATE = '(-|%s)%s-%s' % (CENTURY, YEAR, MONTH)
YEAR_AND_MONTH_DATE_EXTENDED = '-%s%s' % (YEAR, MONTH)
YEAR_ONLY_DATE = '(-|%s)%s' % (CENTURY, YEAR)
CENTURY_ONLY_DATE = CENTURY
DAY_OF_MONTH = '--%s(?:-?%s)?' % (MONTH, DAY)
DAY_ONLY_DATE = '---%s' % DAY
cd_expressions = [
 BASIC_DATE, EXTENDED_DATE, YEAR_AND_MONTH_DATE, YEAR_AND_MONTH_DATE_EXTENDED, YEAR_ONLY_DATE, CENTURY_ONLY_DATE, DAY_OF_MONTH, DAY_ONLY_DATE]
cd_expressions = map(lambda x: '(?P<CalendarDate>%s)' % x, cd_expressions)
ORDINAL_DAY = '(?P<Ordinal>[0-9]{3,3})'
ORDINAL_DATE = '(?P<OrdinalDate>%s?%s-?%s)' % (CENTURY, YEAR, ORDINAL_DAY)
ORDINAL_DATE_ONLY = '(?P<OrdinalDate>-%s)' % ORDINAL_DAY
od_expressions = [ORDINAL_DATE, ORDINAL_DATE_ONLY]
WEEK = '(?P<Week>[0-9][0-9])'
WEEK_DAY = '(?P<Weekday>[1-7])'
BASIC_WEEK_DATE = '%s?%sW%s%s?' % (CENTURY, YEAR, WEEK, WEEK_DAY)
EXTENDED_WEEK_DATE = '%s?%s-W%s(?:-%s)?' % (CENTURY, YEAR, WEEK, WEEK_DAY)
WEEK_IN_DECADE = '-(?P<YearInDecade>[0-9])W%s%s' % (WEEK, WEEK_DAY)
WEEK_IN_DECADE_EXTENDED = '-(?P<YearInDecade>[0-9])-W%s-%s' % (WEEK, WEEK_DAY)
WEEK_AND_DAY_BASIC = '-W%s(?:-?%s)?' % (WEEK, WEEK_DAY)
WEEKDAY_ONLY = '-W?-%s' % WEEK_DAY
wd_expressions = [
 BASIC_WEEK_DATE, EXTENDED_WEEK_DATE, WEEK_IN_DECADE, WEEK_IN_DECADE_EXTENDED, WEEK_AND_DAY_BASIC, WEEKDAY_ONLY]
wd_expressions = map(lambda x: '(?P<WeekDate>%s)' % x, wd_expressions)
date_expressions = map(lambda x: '(?P<Date>%s)' % x, cd_expressions + od_expressions + wd_expressions)
HOUR = '(?P<Hour>(?:0[0-9])|(?:1[0-9])|(?:2[0-4]))'
MINUTE = '(?P<Minute>(?:[0-5][0-9])|(?:60))'
SECOND = '(?P<Second>(?:[0-5][0-9])|(?:60))'
DECIMAL_SEPARATOR = '(?:\\.|,)'
DECIMAL_VALUE = '(?P<DecimalValue>[0-9]*)'
BASIC_TIME_FORMAT = '(?:%s%s%s(?:%s%s)?)' % (HOUR, MINUTE, SECOND, DECIMAL_SEPARATOR, DECIMAL_VALUE)
EXTENDED_TIME_FORMAT = '(?:%s:%s:%s(?:%s%s)?)' % (HOUR, MINUTE, SECOND, DECIMAL_SEPARATOR, DECIMAL_VALUE)
HOUR_MINUTE_TIME = '(?:%s:?%s(?:%s%s)?)' % (HOUR, MINUTE, DECIMAL_SEPARATOR, DECIMAL_VALUE)
HOUR_TIME = '(?:%s(?:%s%s)?)' % (HOUR, DECIMAL_SEPARATOR, DECIMAL_VALUE)
MINUTE_SECOND_TIME = '(?:-%s:?%s(?:%s%s)?)' % (MINUTE, SECOND, DECIMAL_SEPARATOR, DECIMAL_VALUE)
MINUTE_TIME = '(?:-%s(?:%s%s)?)' % (MINUTE, DECIMAL_SEPARATOR, DECIMAL_VALUE)
SECOND_TIME = '(?P<CurrentSecond>--%s(?:%s%s)?)' % (SECOND, DECIMAL_SEPARATOR, DECIMAL_VALUE)
bt_expressions = [
 BASIC_TIME_FORMAT, EXTENDED_TIME_FORMAT, HOUR_MINUTE_TIME, HOUR_TIME, MINUTE_SECOND_TIME, MINUTE_TIME, SECOND_TIME]
bt_expressions = map(lambda x: '(?P<Time>%s)' % x, bt_expressions)
UTC_TIME_ZONE = 'Z'
TZ_DIRECTION = '(?P<TzDirection>\\+|-)'
TZ_HOUR = '(?P<TzHour>(?:0[0-9])|(?:1[0-9])|(?:2[0-4]))'
TZ_MINUTE = '(?P<TzMinute>(?:[0-5][0-9])|(?:60))'
BASIC_TIME_ZONE = '(?P<TzOffset>%s%s(?::?%s)?)' % (TZ_DIRECTION, TZ_HOUR, TZ_MINUTE)
TIME_ZONE = '(?P<TimeZone>%s|%s)' % (UTC_TIME_ZONE, BASIC_TIME_ZONE)
tz_expressions = map(lambda x, t=TIME_ZONE: '%s%s?' % (x, t), bt_expressions)
g_isoExpressions = []
for e in date_expressions:
    g_isoExpressions.append(['^' + e + '$', None])

for e in tz_expressions:
    g_isoExpressions.append(['^' + e + '$', None])

for e in tz_expressions:
    g_isoExpressions.append(['^T' + e + '$', None])

for d in date_expressions:
    for t in tz_expressions:
        g_isoExpressions.append(['^' + d + 'T' + t + '$', None])

del BASIC_DATE
del BASIC_TIME_FORMAT
del BASIC_TIME_ZONE
del BASIC_WEEK_DATE
del CENTURY
del CENTURY_ONLY_DATE
del DAY
del DAY_OF_MONTH
del DAY_ONLY_DATE
del DECIMAL_SEPARATOR
del DECIMAL_VALUE
del EXTENDED_DATE
del EXTENDED_TIME_FORMAT
del EXTENDED_WEEK_DATE
del HOUR
del HOUR_MINUTE_TIME
del HOUR_TIME
del MINUTE
del MINUTE_SECOND_TIME
del MINUTE_TIME
del MONTH
del ORDINAL_DATE
del ORDINAL_DATE_ONLY
del ORDINAL_DAY
del SECOND
del SECOND_TIME
del TIME_ZONE
del TZ_DIRECTION
del TZ_HOUR
del TZ_MINUTE
del UTC_TIME_ZONE
del WEEK
del WEEKDAY_ONLY
del WEEK_AND_DAY_BASIC
del WEEK_DAY
del WEEK_IN_DECADE
del WEEK_IN_DECADE_EXTENDED
del YEAR
del YEAR_AND_MONTH_DATE
del YEAR_AND_MONTH_DATE_EXTENDED
del YEAR_ONLY_DATE
del bt_expressions
del cd_expressions
del d
del date_expressions
del e
del od_expressions
del t
del tz_expressions
del wd_expressions

def FromISO8601(st):
    """
    Create a DT object from an ISO 8601 date, time or date-time string.
    The DT object must contain a complete date and time, and the
    ISO 8601 string might represent a partial date or time, so some
    assumptions are made about the 'implied' information (ISO 8601's
    terminology).
    """
    global g_isoExpressions
    for d in g_isoExpressions:
        (e, c) = d
        if c is None:
            c = re.compile(e)
            d[1] = c
        g = c.match(st)
        if g:
            break
    else:
        raise SyntaxError('Invalid ISO-8601 format: %s' % st)

    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    second = 0
    milliSecond = 0
    tzHourOffset = 0
    tzMinuteOffset = 0
    tzName = ''
    dst = 0
    gd = g.groupdict()
    if gd.has_key('Time'):
        if gd.has_key('Hour'):
            hour = int(gd['Hour'])
        else:
            hour = time.localtime(time.time())[3]
        if gd.has_key('CurrentSecond'):
            minute = time.localtime(time.time())[4]
        else:
            minute = int(gd.get('Minute', 0))
        second = int(gd.get('Second', 0))
        if gd.get('DecimalValue') is not None:
            den = len(gd['DecimalValue']) * 10.0
            val = float(gd['DecimalValue']) / den
            if gd.get('Second') != None:
                milliSecond = val * 1000.0
            elif gd.get('Minute') != None:
                second += int(val * 60.0)
                ms = val * 60.0 - float(int(float(val * 60.0)))
                milliSecond += ms * 100.0
            else:
                minute += int(val * 60.0)
                s = val * 60.0 - float(int(float(val * 60.0)))
                second += s * 60.0
    auto_dst = 0
    if gd.has_key('TimeZone') and gd['TimeZone'] != 'Z' and gd['TimeZone'] != None:
        if gd['TzDirection'] == '-':
            tzMod = -1.0
        else:
            tzMod = 1.0
        tzHourOffset = float(gd['TzHour']) * tzMod
        if gd['TzMinute'] is not None:
            tzMinuteOffset = float(gd['TzMinute']) * tzMod
        hour -= tzHourOffset
        minute -= tzMinuteOffset
    elif gd.has_key('TimeZone') and gd['TimeZone'] == 'Z':
        auto_dst = 1
    thisyear = time.localtime(time.time())[0]
    if gd.get('Date') is not None:
        year = int('%02d%02d' % (int(gd.get('Century') or thisyear / 100), int(gd.get('Year') or thisyear % 100)))
    else:
        year = thisyear
    del thisyear
    if gd.get('CalendarDate') is not None:
        if gd['CalendarDate'][:3] == '---':
            month = time.localtime(time.time())[1]
        else:
            month += int(gd.get('Month', 1))
        day += int(gd.get('Day') or 1)
    elif gd.get('OrdinalDate') is not None:
        month = 1
        day += int(gd.get('Ordinal') or 1)
    elif gd.get('WeekDate') is not None:
        if gd.get('YearInDecade') != None:
            year = int(time.localtime(time.time())[0] / 10.0) * 10
            year += int(gd['YearInDecade'])
        weekDayOfFirst = 1
        y = year
        while y < 2001:
            daysInYear = calendar.isleap(y) and 366 or 365
            weekDayOfFirst = (weekDayOfFirst - daysInYear) % 7
            y += 1

        while y > 2001:
            daysInYear = calendar.isleap(y) and 366 or 365
            weekDayOfFirst = (weekDayOfFirst + daysInYear) % 7
            y -= 1

        if weekDayOfFirst > 4:
            day += 7 - weekDayOfFirst + 1
        else:
            day -= weekDayOfFirst - 1
        month = 1
        day += (int(gd['Week']) - 1) * 7
        day += int(gd['Weekday'] or 1)
    if month == 0:
        month = time.localtime(time.time())[1]
    if day == 0:
        day = time.localtime(time.time())[2]
    if auto_dst:
        dst = isDST((year, month, day, hour, minute, second, 0, 0, -1))
        if dst:
            offset_secs = time.altzone
            tzName = time.tzname[1]
        else:
            offset_secs = time.timezone
            tzName = time.tzname[0]
        tzHourOffset = -offset_secs / 3600
        tzMinuteOffset = abs(offset_secs) % 60
    del auto_dst
    return DT(year, month, day, hour, minute, second, milliSecond, dst, tzName, tzHourOffset, tzMinuteOffset)
    return


def FromRFC822(st):
    """
    Create a DT object from an RFC 822/1123 date string
    """
    t = rfc822.parsedate_tz(st)
    if not t or len(t) != 10:
        raise SyntaxError("Invalid RFC 822 date: '%s'" % st)
    (year, month, day, hour, min, sec, temp, temp, temp, offset) = t
    if year < 100:
        year += 2000
    if offset is None:
        minOff = 0
        hourOff = 0
    else:
        secOff = offset % 60
        minOff = (offset - secOff) / 60.0 % 60
        hourOff = (offset / 60.0 - minOff) / 60.0
    data = st.split()
    if len(data) == 6 or st.count(',') == 1 and len(data) == 5:
        tz = data[(-1)]
    else:
        tz = ''
    return DT(year, month, day, hour - hourOff, min - minOff, sec, 0, 0, tz, hourOff, minOff)
    return


def FromPythonTime(t=None):
    """
    Create a DT object from a float that represents seconds elapsed since the
    local machine's epoch. If not specified, then current time is used.
    """
    if t is None:
        t = time.time()
    if t >= 0:
        return FromPythonTimeTuple(time.gmtime(t))
    else:
        raise ValueError('%r is not a valid time value' % t)
    return


def FromPythonTimeTuple(t):
    """
    Create a DT object from a Python time tuple as documented in the time
    module. This 9-tuple must represent a UTC date and time.
    """
    (year, month, day, hour, minute, second, temp, temp, temp) = t
    if isDST(t):
        offset_secs = time.altzone
        name = time.tzname[1]
    else:
        offset_secs = time.timezone
        name = time.tzname[0]
    hourOff = -offset_secs / 3600
    minOff = abs(offset_secs) % 60
    return DT(year, month, day, hour, minute, second, 0, 0, name, hourOff, minOff)


def isDST(t):
    """
    Indicates whether the given UTC time tuple corresponds to a date
    and time that falls during Daylight Savings Time in the local
    time zone.
    """
    return time.localtime(calendar.timegm(t))[8] == 1