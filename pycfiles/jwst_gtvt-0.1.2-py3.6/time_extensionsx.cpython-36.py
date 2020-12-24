# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/jwst_gtvt/time_extensionsx.py
# Compiled at: 2020-02-10 11:10:52
# Size of source mod 2**32: 9438 bytes
"""Module containing library functions for time manipulation.
Standard for time representation in this project is fractional days.
Dates are represented as modified Julian dates (mjd).
An mjd gives the number of days since midnight on November 17, 1858."""
from math import *
import string
MJD_BASELINE = 2400000.5

def is_leap_year(year):
    """Returns True if the year is a leap year, False otherwise."""
    return year % 4 == 0 and (year % 100 > 0 or year % 400 == 0)


def days_in_year(year):
    """Returns the number of days in a year."""
    days = 365
    if is_leap_year(year):
        days += 1
    return days


def leap_years(year1, year2):
    """Returns the number of leap years between year1 and year2, non-inclusive.
    
    year1 and year2 must be integers, with year2 > year1."""
    next_div4 = int(4 * ceil(year1 / 4.0))
    next_div100 = int(100 * ceil(year1 / 100.0))
    next_div400 = int(400 * ceil(year1 / 400.0))
    div4_years = int(ceil((year2 - next_div4) / 4.0))
    div100_years = int(ceil((year2 - next_div100) / 100.0))
    div400_years = int(ceil((year2 - next_div400) / 400.0))
    return div4_years - (div100_years - div400_years)


def integer_days(time):
    """Takes a time in fractional days and returns integer component."""
    return int(floor(time))


def seconds_into_day(time):
    """Takes a time in fractional days and returns number of seconds since the start of the current day."""
    return int(round(86400.0 * (time % 1)))


def days_to_seconds(days):
    """Takes a time in fractional days and converts it into integer seconds."""
    return int(round(86400 * days))


def seconds_to_days(seconds):
    """Takes a time in integer seconds and converts it into fractional days."""
    return seconds / 86400.0


def round_to_second(time):
    """Rounds a time in days to the nearest second."""
    return round(time * 86400) / 86400.0


def display_time(time, force_hours=False):
    """Returns a string representation of a time specified in fractional days."""
    time = round_to_second(time)
    if time < 0:
        neg_string = '-'
        time = abs(time)
    else:
        neg_string = ''
    days = integer_days(time)
    day_string = hour_string = min_string = ''
    secs_within_day = seconds_into_day(time)
    hours_within_day = int(secs_within_day / 3600)
    secs_within_hour = secs_within_day % 3600
    mins_within_hour = int(secs_within_hour / 60)
    secs_within_min = secs_within_hour % 60
    if days != 0:
        day_string = '%s:' % str(days).zfill(3)
    else:
        if days != 0 or hours_within_day > 0 or force_hours:
            hour_string = '%s:' % str(hours_within_day).zfill(2)
        else:
            if days != 0 or secs_within_day >= 60 or force_hours:
                min_string = '%s:' % str(mins_within_hour).zfill(2)
            if days == 0:
                if hours_within_day == 0 and mins_within_hour == 0:
                    sec_string = '%s' % str(secs_within_min)
        sec_string = '%s' % str(secs_within_min).zfill(2)
    return neg_string + day_string + hour_string + min_string + sec_string


def time_from_string(time_string):
    """Takes a string of the form ddd:hh:mm:ss and converts it to fractional days.
        
    All subfields above seconds are optional and may be omitted if the subfield and
    all higher-order ones are zero."""
    fields = string.split(time_string, ':')
    seconds = int(fields[(-1)])
    num_fields = len(fields)
    minutes = hours = days = 0
    if num_fields > 1:
        minutes = int(fields[(-2)])
        if num_fields > 2:
            hours = int(fields[(-3)])
            if num_fields > 3:
                days = int(fields[(-4)])
    total_seconds = seconds + 60 * minutes + 3600 * hours + 86400 * days
    return seconds_to_days(total_seconds)


def display_date(mjd):
    """Returns a string representation of the date represented by a modified Julian date."""
    int_days = int(floor(321.0 + mjd))
    seconds_in_day = seconds_into_day(mjd)
    fractional_day = mjd % 1
    year = 1858 + int_days / 365
    day_of_year = int_days % 365 - leap_years(1858, year)
    while day_of_year < 1:
        year -= 1
        day_of_year = day_of_year + days_in_year(year)

    year_string = '%s:' % year
    return year_string + display_time(day_of_year + fractional_day)


def compute_mjd(year, day_of_year, hour, minute, second):
    """Computes a modified Julian date from a date specified as a year, day of year, hour, minute, and second.
     
     Arguments should be integers."""
    fractional_days = (hour * 3600 + minute * 60 + second) / 86400.0
    mjd_years = year - 1859
    num_leaps = leap_years(1858, year)
    return 365 * mjd_years + num_leaps + 45 + (day_of_year - 1) + fractional_days


def mjd_from_string(time_string):
    """Takes a string of the form yyyy.ddd:hh:mm:ss and returns an mjd."""
    years = int(time_string[0:4])
    days = int(time_string[5:8])
    hours = int(time_string[9:11])
    minutes = int(time_string[12:14])
    seconds = int(time_string[15:17])
    return compute_mjd(years, days, hours, minutes, seconds)


def mjd_to_jd(mjd):
    """Converts a modified Julian date to a true Julian date."""
    return MJD_BASELINE + mjd


def jd_to_mjd(jd):
    """Converts a Julian date to a modified Julian date."""
    return jd - MJD_BASELINE


class Interval(object):
    __doc__ = 'Class to represent a simple temporal interval.'

    def __init__(self, start, end):
        """Constructor for an interval."""
        self.start = start
        self.end = end

    def __str__(self):
        """Returns a string representation of the interval."""
        return 'Interval: start: %s, end: %s' % (display_date(self.start), display_date(self.end))

    def start_time(self):
        """Returns the start of the interval."""
        return self.start

    def end_time(self):
        """Returns the end of the interval."""
        return self.end

    def duration(self):
        """Returns the duration of an interval in fractional days."""
        return self.end_time() - self.start_time()

    def temporal_relationship(self, time):
        """Returns the temporal relationship between an interval and an absolute time.
        
        Returns 'before' if the interval ends at or before the time,
        'after' if the interval begins at or after the time,
        'includes' if the time occurs during the interval."""
        if self.end_time() <= time:
            rel = 'before'
        else:
            if self.start_time() >= time:
                rel = 'after'
            else:
                rel = 'includes'
        return rel


class FlexibleInterval(Interval):
    __doc__ = 'Class to represent an interval with flexibility on when it can start and end.'

    def __init__(self, est, lst, let):
        """Constructor for a FlexibileInterval.
        
        est = earliest start time (mjd)
        lst = latest start time (mjd)
        let = latest end time (mjd)."""
        self.est = est
        self.lst = lst
        self.let = let

    def __str__(self):
        """Returns a string representation of the FlexibleInterval."""
        return 'FlexibleInterval: EST: %s, LST: %s, LET: %s' % (
         display_date(self.est), display_date(self.lst), display_date(self.let))

    def start_time(self):
        """Returns the start of the FlexibleInterval."""
        return self.est

    def end_time(self):
        """Returns the end of the FlexibleInterval."""
        return self.let

    def flexibility(self):
        """Returns the flexibility of the FlexibleInterval, in fractional days."""
        return self.lst - self.est

    def maximum_duration(self):
        """Returns the maximum duration of the FlexibleInterval, in fractional days."""
        return self.let - self.lst