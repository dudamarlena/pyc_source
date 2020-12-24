# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/context/expressiontime.py
# Compiled at: 2016-12-15 12:36:10
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from ..compat import implements_to_string, text_type, string_types, number_types, implements_bool
from ..interface import AttributeExposer
from .. import interface
from ..tools import parse_timedelta
from .. import pilot
from ..context.expressionrange import ExpressionRange
from datetime import date, time, datetime, timedelta
from calendar import monthrange, timegm
from math import floor
import re, iso8601
from babel.dates import format_datetime, format_date, format_time, format_timedelta, parse_pattern
import calendar
from pytz import UTC, timezone
utcfromtimestamp = datetime.utcfromtimestamp
utclocalize = UTC.localize
GMT = timezone(b'GMT')

def datetime_to_epoch(d):
    """Convert datetime to epoch"""
    return timegm(d.utctimetuple())


def epoch_to_datetime(t):
    """Convert epoch time to a UTC datetime"""
    return utclocalize(utcfromtimestamp(t))


class DatetimeExclusiveRange(ExpressionRange):

    def _build(self, start, end):
        self.start = start
        self.end = end
        self.step = timedelta(days=1)
        self._forward = end >= start

    def __iter__(self):
        if self._forward:
            d = self.start
            while d < self.end:
                yield d
                d += self.step

        else:
            d = self.start
            while d > self.end:
                yield d
                d -= self.step

    def __moyacall__(self, params):
        step = params.get(b'step', None)
        if step is not None:
            self.step = timedelta(milliseconds=step)
        return self

    def __contains__(self, v):
        if self._forward:
            return v >= self.start and v < self.stop
        else:
            return v <= self.start and v > self.stop


class DatetimeInclusiveRange(DatetimeExclusiveRange):

    def __iter__(self):
        if self._forward:
            d = self.start
            while d <= self.end:
                yield d
                d += self.step

        else:
            d = self.start
            while d >= self.end:
                yield d
                d -= self.step


class ExpressionDate(date, interface.Proxy):

    @classmethod
    def from_sequence(self, seq):
        try:
            year, month, day = (int(s) for s in seq)
        except ValueError:
            raise ValueError(b'[year, month, day] should be integers')
        except:
            raise ValueError(b'[year, month, day] required')

        return ExpressionDate(year, month, day).moya_proxy

    @classmethod
    def from_date(self, d):
        return ExpressionDate(d.year, d.month, d.day).moya_proxy

    @classmethod
    def from_isoformat(cls, s):
        if isinstance(s, date):
            return cls.from_date(s)
        else:
            if isinstance(s, ExpressionDateTime):
                return s.date
            try:
                dt = iso8601.parse_date(s)
                return cls.from_date(dt.date())
            except:
                return

            return

    def __moyadbobject__(self):
        return date(self.year, self.month, self.day)

    @implements_to_string
    class ProxyInterface(AttributeExposer):
        __moya_exposed_attributes__ = [b'year', b'month', b'day',
         b'next_month', b'previous_month',
         b'isoformat', b'next_day', b'previous_day',
         b'leap']

        def __init__(self, obj):
            self.date = obj

        def __hash__(self):
            return hash(interface.unproxy(self))

        def __moyapy__(self):
            return self.date

        def __moyajson__(self):
            return self.isoformat

        def __format__(self, fmt):
            return format(self.date, fmt)

        def __str__(self):
            return self.isoformat

        def __repr__(self):
            return (b'<date "{}">').format(self.isoformat)

        def __moyarepr__(self, context):
            return (b"date:'{}'").format(self.isoformat)

        def __moyalocalize__(self, context, locale):
            fmt = context.get(b'.sys.site.date_format', b'medium')
            return format_date(self.date, format=fmt, locale=text_type(locale))

        def __moyarange__(self, context, end, inclusive=False):
            if inclusive:
                return DatetimeInclusiveRange(context, self, end)
            else:
                return DatetimeExclusiveRange(context, self, end)

        def __moyaconsole__(self, console):
            console(self.isoformat).nl()

        def __mod__(self, fmt):
            return format_date(self.date, format=fmt, locale=text_type(pilot.context.get(b'.locale', b'en_US')))

        @property
        def year(self):
            return self.date.year

        @property
        def month(self):
            return self.date.month

        @property
        def day(self):
            return self.date.day

        @property
        def isoformat(self):
            return self.date.isoformat()

        @property
        def next_day(self):
            return ExpressionDate.from_date(self.date + timedelta(days=1))

        @property
        def previous_day(self):
            return ExpressionDate.from_date(self.date + timedelta(days=-1))

        @property
        def next_month(self):
            """The first date in the following month"""
            d = self.date
            if d.month == 12:
                return ExpressionDate(d.year + 1, 1)
            else:
                return ExpressionDate(d.year, d.month + 1, 1)

        @property
        def previous_month(self):
            """First date in the previous month"""
            d = self.date
            if d.month == 1:
                return ExpressionDate(d.year - 1, 12, 1)
            else:
                return ExpressionDate(d.year, d.month - 1, 1)

        @property
        def leap(self):
            return calendar.isleap(self.year)

        def __sub__(self, other):
            dt = self.date
            other = interface.unproxy(other)
            result = dt - other
            if isinstance(result, date):
                return ExpressionDate.from_date(result)
            else:
                if isinstance(result, (timedelta, TimeSpan)):
                    return TimeSpan.from_timedelta(result)
                return result

        def __add__(self, other):
            dt = self.date
            other = interface.unproxy(other)
            if isinstance(other, time):
                return ExpressionDateTime.combine(self.date, other)
            else:
                result = dt + other
                if isinstance(result, date):
                    return ExpressionDate.from_date(result)
                if isinstance(result, (timedelta, TimeSpan)):
                    return TimeSpan.from_timedelta(result)
                return result

        def __eq__(self, other):
            return interface.unproxy(self) == interface.unproxy(other)

        def __ne__(self, other):
            return interface.unproxy(self) != interface.unproxy(other)

        def __lt__(self, other):
            return interface.unproxy(self) < interface.unproxy(other)

        def __le__(self, other):
            return interface.unproxy(self) <= interface.unproxy(other)

        def __gt__(self, other):
            return interface.unproxy(self) > interface.unproxy(other)

        def __ge__(self, other):
            return interface.unproxy(self) >= interface.unproxy(other)


class ExpressionTime(time, interface.Proxy):
    _re_time = re.compile(b'^(\\d\\d)\\:(\\d\\d)(?:\\:(\\d{1,2}\\.?\\d+?))?$')

    @classmethod
    def from_time(self, t):
        return ExpressionTime(t.hour, t.minute, t.second, t.microsecond, t.tzinfo).moya_proxy

    @classmethod
    def from_isoformat(cls, t):
        t = interface.unproxy(t)
        if isinstance(t, time):
            return cls.from_time(t)
        else:
            if isinstance(t, ExpressionDateTime):
                return t.time.moya_proxy
            try:
                hour, minute, second = cls._re_time.match(t).groups()
                microsecond = 0
                if b'.' in second:
                    second, fraction = second.split(b'.', 1)
                    fraction = float(fraction)
                    if fraction:
                        microsecond = int(1.0 / fraction * 1000000)
                time_obj = time(int(hour), int(minute), int(second), int(microsecond))
                return cls.from_time(time_obj)
            except:
                return

            return

    @implements_to_string
    class ProxyInterface(AttributeExposer):
        __moya_exposed_attributes__ = [
         b'hour', b'minute', b'second', b'microsecond',
         b'tzinfo',
         b'isoformat']

        def __init__(self, obj):
            self.time = obj

        def __hash__(self):
            return hash(interface.unproxy(self))

        def __moyapy__(self):
            return self.time

        def __moyajson__(self):
            return self.isoformat

        def __format__(self, fmt):
            return format(self.time, fmt)

        def __str__(self):
            return self.isoformat

        def __repr__(self):
            return (b'<time "{}">').format(self.isoformat)

        def __moyarepr__(self, context):
            return (b"time:'{}'").format(self.isoformat)

        def __moyalocalize__(self, context, locale):
            fmt = context.get(b'.sys.site.time_format', b'medium')
            return format_time(self.time, fmt, locale=text_type(locale))

        def __moyaconsole__(self, console):
            console(self.isoformat).nl()

        def __getattr__(self, k):
            if k in self.__moya_exposed_attributes__:
                return getattr(self.time, k)
            raise AttributeError(k)

        def __mod__(self, fmt):
            try:
                return format_time(self.time, fmt, locale=text_type(pilot.context.get(b'.locale', b'en_US')))
            except:
                raise ValueError((b"'{}' is not a valid time format string").format(fmt))

        @property
        def isoformat(self):
            return self.time.isoformat()

        def __eq__(self, other):
            return interface.unproxy(self) == interface.unproxy(other)

        def __ne__(self, other):
            return interface.unproxy(self) != interface.unproxy(other)

        def __lt__(self, other):
            return interface.unproxy(self) < interface.unproxy(other)

        def __le__(self, other):
            return interface.unproxy(self) <= interface.unproxy(other)

        def __gt__(self, other):
            return interface.unproxy(self) > interface.unproxy(other)

        def __ge__(self, other):
            return interface.unproxy(self) >= interface.unproxy(other)


class ExpressionDateTime(datetime, interface.Proxy):

    @classmethod
    def moya_utcnow(self):
        return self.ProxyInterface.utcnow()

    @classmethod
    def from_datetime(cls, dt):
        return cls.ProxyInterface(dt)

    @classmethod
    def from_isoformat(cls, s):
        if isinstance(s, number_types):
            return cls.from_datetime(datetime.fromtimestamp(s))
        else:
            if isinstance(s, datetime):
                return cls.from_datetime(s)
            if isinstance(s, ExpressionDateTime):
                return s
            try:
                dt = iso8601.parse_date(s)
                return cls.from_datetime(dt)
            except:
                return

            return

    @classmethod
    def from_ctime(cls, s):
        try:
            dt = cls.strptime(text_type(s), b'%a %b %d %H:%M:%S %Y')
            return cls.from_datetime(dt)
        except:
            return

        return

    @classmethod
    def from_epoch(cls, epoch):
        return cls.ProxyInterface(epoch_to_datetime(epoch))

    @classmethod
    def parse(cls, t, pattern):
        try:
            dt = datetime.strptime(t, pattern)
            return cls.from_datetime(dt)
        except:
            return

        return

    def __moyarepr__(self, context):
        return (b"datetime:'{}'").format(self.isoformat())

    def __moyadbobject__(self):
        dt = self.moya_proxy.utc.naive
        dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)
        return dt

    @implements_to_string
    class ProxyInterface(AttributeExposer):
        __moya_exposed_attributes__ = [
         b'year', b'month', b'day', b'minute', b'hour', b'second', b'microsecond', b'tzinfo',
         b'date', b'time',
         b'year_start', b'month_start', b'day_start',
         b'next_day', b'next_year', b'next_month',
         b'previous_day', b'previous_month', b'previous_year',
         b'leap',
         b'days_in_month', b'epoch',
         b'isoformat', b'local', b'utc', b'naive',
         b'html5_datetime', b'html5_date', b'html5_time',
         b'rfc2822', b'http_date']
        _re_date = re.compile(b'^(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)$')
        _re_time = re.compile(b'^(\\d\\d)\\:(\\d\\d)(?:\\:(\\d{1,2}\\.?\\d+?))?$')

        def __init__(self, obj):
            self._dt = obj

        def __hash__(self):
            return hash(interface.unproxy(self))

        def __moyarepr__(self, context):
            return (b"datetime:'{}'").format(self.isoformat)

        def __moyapy__(self):
            return self._dt

        def __moyajson__(self):
            return self.isoformat

        def __moyaconsole__(self, console):
            console.text(text_type(self.ctime()))

        def __moyarange__(self, context, end, inclusive=False):
            if inclusive:
                return DatetimeInclusiveRange(context, self, end)
            else:
                return DatetimeExclusiveRange(context, self, end)

        def __str__(self):
            return self.isoformat

        def __repr__(self):
            return (b'<datetime "{}">').format(self.isoformat)

        def __format__(self, fmt):
            return format(self._dt, fmt)

        def __moyalocalize__(self, context, locale):
            fmt = context.get(b'.sys.site.datetime_format', b'medium')
            return format_datetime(self.local._dt, format=fmt, locale=text_type(locale))

        def __moyadbobject__(self):
            dt = self.utc.naive
            dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)
            return dt

        def __getattr__(self, key):
            return getattr(self._dt, key)

        @classmethod
        def utcnow(cls):
            now = ExpressionDateTime.from_datetime(datetime.utcnow())
            return now

        @classmethod
        def from_datetime(cls, dt):
            return ExpressionDateTime.from_datetime(dt)

        @classmethod
        def make(cls, *args, **kwargs):
            return cls(datetime(*args, **kwargs))

        @classmethod
        def from_html5(cls, s):
            if isinstance(s, datetime):
                return cls.from_datetime(s)
            if isinstance(s, ExpressionDateTime):
                return s
            s = text_type(s)
            if b'T' in s:
                date_s, time_s = s.split(b'T', 1)
            else:
                date_s = s
                time_s = b'00:00'
            try:
                year, month, day = cls._re_date.match(date_s).groups()
                hour, minute, second = cls._re_time.match(time_s).groups()
            except AttributeError:
                raise ValueError((b"Could not parse '{}' as a html5 date/time").format(s))

            second = float(second or 0.0)
            microsecond = int(floor(second * 1000000) % 1000000)
            return ExpressionDateTime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

        @property
        def date(self):
            dt = self._dt
            return ExpressionDate(dt.year, dt.month, dt.day)

        @property
        def time(self):
            dt = self._dt
            return ExpressionTime(dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

        @property
        def year_start(self):
            """Start of the year"""
            dt = self._dt
            return ExpressionDateTime(dt.year, 1, 1, tzinfo=dt.tzinfo)

        @property
        def month_start(self):
            """Start of the month"""
            dt = self._dt
            return ExpressionDateTime(dt.year, dt.month, 1, tzinfo=dt.tzinfo)

        @property
        def day_start(self):
            """Start of the day"""
            dt = self._dt
            return ExpressionDateTime(dt.year, dt.month, dt.day, tzinfo=dt.tzinfo)

        @property
        def next_year(self):
            """First date in the following year"""
            dt = self._dt
            return ExpressionDateTime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)

        @property
        def next_month(self):
            """The first date in the following month"""
            dt = self._dt
            if dt.month == 12:
                return ExpressionDateTime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)
            else:
                return ExpressionDateTime(dt.year, dt.month + 1, 1, tzinfo=dt.tzinfo)

        @property
        def next_day(self):
            """The start of the following day"""
            return self.from_datetime(self._dt + timedelta(hours=24)).day_start

        @property
        def previous_day(self):
            return self.from_datetime(self._dt - timedelta(hours=24)).day_start

        @property
        def previous_year(self):
            """First date in the previous year"""
            dt = self._dt
            return ExpressionDateTime(dt.year - 1, 1, 1, tzinfo=dt.tzinfo)

        @property
        def previous_month(self):
            """First date in the previous month"""
            dt = self._dt
            if dt.month == 1:
                return ExpressionDateTime(dt.year - 1, 12, 1, tzinfo=dt.tzinfo)
            else:
                return ExpressionDateTime(dt.year, dt.month - 1, 1, tzinfo=dt.tzinfo)

        @property
        def leap(self):
            return calendar.isleap(self.date.year)

        @property
        def days_in_month(self):
            dt = self._dt
            _, maxdays = monthrange(dt.year, dt.month)
            return maxdays

        @property
        def epoch(self):
            return datetime_to_epoch(self._dt)

        @property
        def html5_datetime(self):
            return (b'{}T{}').format(self.html5_date, self.html5_time)

        @property
        def html5_date(self):
            dt = self._dt
            fmt = b'{:04}-{:02}-{:02}'
            return fmt.format(dt.year, dt.month, dt.day)

        @property
        def html5_time(self):
            dt = self._dt
            fmt = b'{:02}:{:02}'
            return fmt.format(dt.hour, dt.minute)

        @property
        def isoformat(self):
            dt = self._dt
            return datetime.isoformat(dt)

        @property
        def rfc2822(self):
            from email import utils
            return utils.formatdate(self.epoch)

        @property
        def http_date(self):
            dt = self._dt
            gmt_time = GMT.localize(dt)
            return gmt_time.strftime(b'%a, %d %b %Y %H:%M:%S GMT')

        @property
        def utc(self):
            dt = self._dt
            if dt.tzinfo is None:
                return self.from_datetime(UTC.localize(dt))
            else:
                return self.from_datetime(dt.astimezone(UTC))

        @property
        def naive(self):
            dt = self._dt
            return self.make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)

        @property
        def local(self):
            tz = pilot.context.get(b'.tz', None)
            if tz is None:
                return
            else:
                return self.from_datetime(tz(self._dt))

        def __mod__(self, fmt):
            self = self._dt
            return format_datetime(self, fmt, locale=text_type(pilot.context.get(b'.locale', b'en_US')))

        def __sub__(self, other):
            dt = self._dt
            result = dt - interface.unproxy(other)
            if isinstance(result, datetime):
                return ExpressionDateTime.from_datetime(result)
            else:
                if isinstance(result, (timedelta, TimeSpan)):
                    return TimeSpan.from_timedelta(result)
                return result

        def __add__(self, other):
            dt = self._dt
            result = dt + interface.unproxy(other)
            if isinstance(result, datetime):
                return ExpressionDateTime.from_datetime(result)
            else:
                if isinstance(result, (timedelta, TimeSpan)):
                    return TimeSpan.from_timedelta(result)
                return result

        def __eq__(self, other):
            return interface.unproxy(self) == interface.unproxy(other)

        def __ne__(self, other):
            return interface.unproxy(self) != interface.unproxy(other)

        def __lt__(self, other):
            return interface.unproxy(self) < interface.unproxy(other)

        def __le__(self, other):
            return interface.unproxy(self) <= interface.unproxy(other)

        def __gt__(self, other):
            return interface.unproxy(self) > interface.unproxy(other)

        def __ge__(self, other):
            return interface.unproxy(self) >= interface.unproxy(other)


def to_milliseconds(value):
    if isinstance(value, TimeSpan):
        return int(TimeSpan(value).milliseconds)
    else:
        if value is not None:
            return int(value)
        else:
            return

        return


def to_seconds(value):
    if isinstance(value, TimeSpan):
        return int(TimeSpan(value).seconds)
    else:
        if value is not None:
            return int(value)
        else:
            return

        return


@implements_bool
@implements_to_string
class TimeSpan(object):

    def __init__(self, ms=0):
        if isinstance(ms, string_types):
            self._ms = float(sum(parse_timedelta(token) for token in ms.split()))
        else:
            self._ms = float(ms)

    def __str__(self):
        return self.text

    def __repr__(self):
        return b"TimeSpan('%s')" % self.simplify

    def __moyarepr__(self, context):
        return self.simplify

    @classmethod
    def from_timedelta(cls, time_delta):
        if isinstance(time_delta, TimeSpan):
            return TimeSpan(time_delta._ms)
        return TimeSpan(time_delta.total_seconds() * 1000.0)

    @classmethod
    def to_ms(cls, value):
        if isinstance(value, string_types):
            return parse_timedelta(value)
        else:
            return int(value)

    @property
    def simplify(self):
        """Units in lowest common denominator"""
        ms = self._ms
        for unit, divisible in [(b'd', 86400000),
         (
          b'h', 3600000),
         (
          b'm', 60000),
         ('s', 1000),
         ('ms', 1)]:
            if not ms % divisible:
                return (b'{}{}').format(ms // divisible, unit)

    def __moyalocalize__(self, context, locale):
        fmt = context.get(b'.sys.site.timespan_format', b'medium')
        td = timedelta(milliseconds=self._ms)
        return format_timedelta(td, format=fmt, locale=text_type(locale))

    @property
    def text(self):
        """Nice textual representation of a time span"""
        ms = self._ms
        text = []
        for name, plural, divisable in [(b'day', b'days', 86400000),
         (
          b'hour', b'hours', 3600000),
         (
          b'minute', b'minutes', 60000),
         ('second', 'seconds', 1000),
         ('millisecond', 'milliseconds', 1)]:
            unit = ms // divisable
            if unit:
                if unit == 1:
                    text.append(b'%i %s' % (unit, name))
                else:
                    text.append(b'%i %s' % (unit, plural))
            ms -= unit * divisable

        if not text:
            return b'0 seconds'
        else:
            return (b', ').join(text)

    @property
    def milliseconds(self):
        return self._ms

    @property
    def seconds(self):
        return self._ms // 1000

    @property
    def minutes(self):
        return self._ms // 60000

    @property
    def hours(self):
        return self._ms // 3600000

    @property
    def days(self):
        return self._ms // 86400000

    def __int__(self):
        return int(self._ms)

    def __float__(self):
        return float(self._ms / 1000.0)

    def __bool__(self):
        return bool(self._ms)

    def __add__(self, other):
        if isinstance(other, datetime):
            return ExpressionDateTime.from_datetime(other + timedelta(milliseconds=self._ms))
        if isinstance(other, date):
            return ExpressionDate.from_date(other + timedelta(milliseconds=self._ms))
        return TimeSpan(self._ms + self.to_ms(other))

    def __sub__(self, other):
        if isinstance(other, datetime):
            return ExpressionDateTime.from_datetime(other - timedelta(milliseconds=self._ms))
        return TimeSpan(self._ms - self.to_ms(other))

    def __mul__(self, other):
        return TimeSpan(self._ms * float(other))

    def __eq__(self, other):
        return self._ms == self.to_ms(other)

    def __rmul__(self, other):
        return TimeSpan(self._ms * float(other))

    def __radd__(self, other):
        if isinstance(other, datetime):
            return ExpressionDateTime.from_datetime(other + timedelta(milliseconds=self._ms))
        else:
            if isinstance(other, date):
                return ExpressionDate.from_date(other + timedelta(milliseconds=self._ms))
            return self + self.to_ms(other)

    def __rsub__(self, other):
        if isinstance(other, datetime):
            return ExpressionDateTime.from_datetime(other - timedelta(milliseconds=self._ms))
        else:
            if isinstance(other, date):
                return ExpressionDate.from_date(other - timedelta(milliseconds=self._ms))
            return self - self.to_ms(other)

    def __neg__(self):
        return TimeSpan(-self._ms)

    def __pos__(self):
        return TimeSpan(+self._ms)

    def __abs__(self):
        return TimeSpan(abs(self._ms))

    def __ne__(self, other):
        return self._ms != self.to_ms(other)

    def __lt__(self, other):
        return self._ms < self.to_ms(other)

    def __le__(self, other):
        return self._ms <= self.to_ms(other)

    def __gt__(self, other):
        return self._ms > self.to_ms(other)

    def __ge__(self, other):
        return self._ms >= self.to_ms(other)


if __name__ == b'__main__':
    n = ExpressionDateTime.now()
    print(n.isoformat)
    d = n.isoformat.replace(b'T', b' ')
    print(ExpressionDateTime.from_isoformat(d).isoformat)