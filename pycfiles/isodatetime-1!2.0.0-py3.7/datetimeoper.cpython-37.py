# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/isodatetime/datetimeoper.py
# Compiled at: 2019-01-30 07:03:09
# Size of source mod 2**32: 12528 bytes
"""High level common date-time point and duration utilities."""
from datetime import datetime
import os
from .data import Calendar, get_timepoint_for_now
from .dumpers import TimePointDumper
from .parsers import TimePointParser, DurationParser, TimeRecurrenceParser

class OffsetValueError(ValueError):
    __doc__ = 'Bad offset value.'

    def __str__(self):
        return '%s: bad offset value' % self.args[0]


class DateTimeOperator(object):
    __doc__ = 'A class to parse and print date string with an offset.'
    CURRENT_TIME_DUMP_FORMAT = 'CCYY-MM-DDThh:mm:ss+hh:mm'
    CURRENT_TIME_DUMP_FORMAT_Z = 'CCYY-MM-DDThh:mm:ssZ'
    ENV_REF = 'ISODATETIMEREF'
    ENV_CALENDAR_MODE = 'ISODATETIMECALENDAR'
    PARSE_FORMATS = [
     '%a %b %d %H:%M:%S %Y',
     '%a %d %b %H:%M:%S %Z %Y',
     '%Y-%m-%dT%H:%M:%S',
     '%Y%m%dT%H%M%S']
    STR_NOW = 'now'
    STR_REF = 'ref'
    UNITS = {'w':'weeks', 
     'd':'days', 
     'h':'hours', 
     'm':'minutes', 
     's':'seconds'}

    def __init__(self, parse_format=None, utc_mode=False, calendar_mode=None, ref_point_str=None):
        """Constructor.

        parse_format -- If specified, parse with the specified format.
                        Otherwise, parse with one of the format strings in
                        self.PARSE_FORMATS. The format should be a string
                        compatible to strptime(3).

        utc_mode -- If True, parse/print in UTC mode rather than local or
                    other timezones.

        calendar_mode -- Set calendar mode, for isodatetime.data.Calendar.

        ref_point_str -- Set the reference time point for operations.
                         If not specified, operations use current date time.

        """
        self.parse_formats = self.PARSE_FORMATS
        self.custom_parse_format = parse_format
        self.utc_mode = utc_mode
        if self.utc_mode:
            assumed_time_zone = (0, 0)
        else:
            assumed_time_zone = None
        if not calendar_mode:
            calendar_mode = os.getenv(self.ENV_CALENDAR_MODE)
        else:
            self.set_calendar_mode(calendar_mode)
            self.time_point_dumper = TimePointDumper()
            self.time_point_parser = TimePointParser(assumed_time_zone=assumed_time_zone)
            self.duration_parser = DurationParser()
            self.recurrence_parser = TimeRecurrenceParser(self.time_point_parser, self.duration_parser)
            if ref_point_str is None:
                self.ref_point_str = os.getenv(self.ENV_REF)
            else:
                self.ref_point_str = ref_point_str

    def date_format(self, print_format, time_point):
        """Reformat time_point according to print_format.

        time_point -- The time point to format.

        """
        if '%' in print_format:
            return self.strftime(time_point, print_format)
        return self.time_point_dumper.dump(time_point, print_format)

    def date_parse(self, time_point_str=None):
        """Parse time_point_str.

        Return (t, format) where t is a isodatetime.data.TimePoint object and
        format is the format that matches time_point_str.

        time_point_str -- The time point string to parse.
                          Otherwise, use ref time.

        """
        if time_point_str == self.STR_REF:
            time_point_str = self.ref_point_str
        elif time_point_str is None or time_point_str == self.STR_NOW:
            time_point = get_timepoint_for_now()
            time_point.set_time_zone_to_local()
            if self.utc_mode or time_point.get_time_zone_utc():
                parse_format = self.CURRENT_TIME_DUMP_FORMAT_Z
            else:
                parse_format = self.CURRENT_TIME_DUMP_FORMAT
        elif self.custom_parse_format is not None:
            parse_format = self.custom_parse_format
            time_point = self.strptime(time_point_str, parse_format)
        else:
            time_point = None
            for parse_format in self.parse_formats:
                try:
                    time_point = self.strptime(time_point_str, parse_format)
                    break
                except ValueError:
                    pass

            if time_point is None:
                time_point = self.time_point_parser.parse(time_point_str,
                  dump_as_parsed=True)
                parse_format = time_point.dump_format
        if self.utc_mode:
            time_point.set_time_zone_to_utc()
        return (
         time_point, parse_format)

    def date_shift(self, time_point, offset=None):
        """Return a date string with an offset.

        time_point -- A time point or time point string.
                      Otherwise, use current time.

        offset -- If specified, it should be a string containing the offset
                  that has the format "[+/-]nU[nU...]" where "n" is an
                  integer, and U is a unit matching a key in self.UNITS.

        """
        if offset:
            sign = '+'
            if offset.startswith('-') or offset.startswith('+'):
                sign = offset[0]
                offset = offset[1:]
            else:
                try:
                    duration = self.duration_parser.parse(offset)
                except ValueError:
                    raise OffsetValueError(offset)

                if sign == '-':
                    time_point -= duration
                else:
                    time_point += duration
        return time_point

    @staticmethod
    def date_diff(time_point_1=None, time_point_2=None):
        """Return (duration, is_negative) between two TimePoint objects.

        duration -- is a Duration instance.
        is_negative -- is "-" if time_point_2 is in the past of time_point_1.
        """
        if time_point_2 < time_point_1:
            return (
             time_point_1 - time_point_2, '-')
        return (time_point_2 - time_point_1, '')

    @staticmethod
    def date_diff_format(print_format, duration, sign):
        """Format a duration."""
        if print_format:
            delta_lookup = {'y':duration.years,  'm':duration.months, 
             'd':duration.days, 
             'h':duration.hours, 
             'M':duration.minutes, 
             's':duration.seconds}
            expression = ''
            for item in print_format:
                if item not in delta_lookup:
                    expression += item
                elif float(delta_lookup[item]).is_integer():
                    expression += str(int(delta_lookup[item]))
                else:
                    expression += str(delta_lookup[item])

            return sign + expression
        return sign + str(duration)

    @staticmethod
    def get_calendar_mode():
        """Get current calendar mode."""
        return Calendar.default().mode

    @staticmethod
    def set_calendar_mode(calendar_mode):
        """Set calendar mode for subsequent operations.

        Raise KeyError if calendar_mode is invalid.

        """
        Calendar.default().set_mode(calendar_mode)

    def strftime(self, time_point, print_format):
        """Use either the isodatetime or datetime strftime time formatting."""
        try:
            return time_point.strftime(print_format)
        except ValueError:
            return self.get_datetime_strftime(time_point, print_format)

    def strptime(self, time_point_str, parse_format):
        """Use either the isodatetime or datetime strptime time parsing."""
        try:
            return self.time_point_parser.strptime(time_point_str, parse_format)
        except ValueError:
            return self.get_datetime_strptime(time_point_str, parse_format)

    @staticmethod
    def get_datetime_strftime(time_point, print_format):
        """Use the datetime library's strftime as a fallback."""
        calendar_date = time_point.copy().to_calendar_date()
        year, month, day = calendar_date.get_calendar_date()
        hour, minute, second = time_point.get_hour_minute_second()
        microsecond = int(1000000.0 * (second - int(second)))
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        date_time = datetime(year, month, day, hour, minute, second, microsecond)
        return date_time.strftime(print_format)

    def get_datetime_strptime(self, time_point_str, parse_format):
        """Use the datetime library's strptime as a fallback."""
        date_time = datetime.strptime(time_point_str, parse_format)
        return self.time_point_parser.parse(date_time.isoformat())

    def process_time_point_str(self, time_point_str=None, offsets=None, print_format=None):
        """Process time point string with optional offsets."""
        time_point, parse_format = self.date_parse(time_point_str)
        if offsets:
            for offset in offsets:
                time_point = self.date_shift(time_point, offset)

        if print_format:
            return self.date_format(print_format, time_point)
        return self.date_format(parse_format, time_point)

    def diff_time_point_strs(self, time_point_str1, time_point_str2, offsets1=None, offsets2=None, print_format=None, duration_print_format=None):
        """Calculate duration between 2 time point strings.

        Each time point string may have optional offsets.
        """
        time_point1 = self.date_parse(time_point_str1)[0]
        time_point2 = self.date_parse(time_point_str2)[0]
        if offsets1:
            for offset in offsets1:
                time_point1 = self.date_shift(time_point1, offset)

        if offsets2:
            for offset in offsets2:
                time_point2 = self.date_shift(time_point2, offset)

        duration, sign = self.date_diff(time_point1, time_point2)
        out = self.date_diff_format(print_format, duration, sign)
        if duration_print_format:
            return self.format_duration_str(out, duration_print_format)
        return out

    def format_duration_str(self, duration_str, duration_print_format):
        """Parse duration string, return as total of a unit.

        Unit can be H, M or S (for hours, minutes or seconds).
        """
        duration = self.duration_parser.parse(duration_str.replace('\\', ''))
        time = duration.get_seconds()
        options = {'S':time,  'M':time / 60,  'H':time / 3600}
        if duration_print_format.upper() in options:
            return options[duration_print_format.upper()]
        raise ValueError('Invalid duration print format, should use one of H, M, S for (hours, minutes, seconds)')

    def iter_recurrence_str(self, recurrence_str, print_format=None):
        """Parse recurrence string, return time point strings iterator."""
        recurrence = self.recurrence_parser.parse(recurrence_str)
        for time_point in recurrence:
            yield self.strftime(time_point, print_format)