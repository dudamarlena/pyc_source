# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/dates.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 9536 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from airflow.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import six
from croniter import croniter
cron_presets = {'@hourly':'0 * * * *', 
 '@daily':'0 0 * * *', 
 '@weekly':'0 0 * * 0', 
 '@monthly':'0 0 1 * *', 
 '@yearly':'0 0 1 1 *'}

def date_range(start_date, end_date=None, num=None, delta=None):
    """
    Get a set of dates as a list based on a start, end and delta, delta
    can be something that can be added to `datetime.datetime`
    or a cron expression as a `str`

    .. code-block:: python

        date_range(datetime(2016, 1, 1), datetime(2016, 1, 3), delta=timedelta(1))
            [datetime.datetime(2016, 1, 1, 0, 0), datetime.datetime(2016, 1, 2, 0, 0),
            datetime.datetime(2016, 1, 3, 0, 0)]
        date_range(datetime(2016, 1, 1), datetime(2016, 1, 3), delta='0 0 * * *')
            [datetime.datetime(2016, 1, 1, 0, 0), datetime.datetime(2016, 1, 2, 0, 0),
            datetime.datetime(2016, 1, 3, 0, 0)]
        date_range(datetime(2016, 1, 1), datetime(2016, 3, 3), delta="0 0 0 * *")
            [datetime.datetime(2016, 1, 1, 0, 0), datetime.datetime(2016, 2, 1, 0, 0),
            datetime.datetime(2016, 3, 1, 0, 0)]

    :param start_date: anchor date to start the series from
    :type start_date: datetime.datetime
    :param end_date: right boundary for the date range
    :type end_date: datetime.datetime
    :param num: alternatively to end_date, you can specify the number of
        number of entries you want in the range. This number can be negative,
        output will always be sorted regardless
    :type num: int
    """
    if not delta:
        return []
    else:
        if end_date:
            if start_date > end_date:
                raise Exception('Wait. start_date needs to be before end_date')
            else:
                if end_date:
                    if num:
                        raise Exception('Wait. Either specify end_date OR num')
                if not end_date:
                    if not num:
                        end_date = timezone.utcnow()
        else:
            delta_iscron = False
            tz = start_date.tzinfo
            if isinstance(delta, six.string_types):
                delta_iscron = True
                start_date = timezone.make_naive(start_date, tz)
                cron = croniter(delta, start_date)
            else:
                if isinstance(delta, timedelta):
                    delta = abs(delta)
            dates = []
            if end_date:
                if timezone.is_naive(start_date):
                    end_date = timezone.make_naive(end_date, tz)
                while start_date <= end_date:
                    if timezone.is_naive(start_date):
                        dates.append(timezone.make_aware(start_date, tz))
                    else:
                        dates.append(start_date)
                    if delta_iscron:
                        start_date = cron.get_next(datetime)
                    else:
                        start_date += delta

            else:
                for _ in range(abs(num)):
                    if timezone.is_naive(start_date):
                        dates.append(timezone.make_aware(start_date, tz))
                    else:
                        dates.append(start_date)
                    if delta_iscron:
                        if num > 0:
                            start_date = cron.get_next(datetime)
                        else:
                            start_date = cron.get_prev(datetime)
                    else:
                        if num > 0:
                            start_date += delta
                        else:
                            start_date -= delta

        return sorted(dates)


def round_time(dt, delta, start_date=timezone.make_aware(datetime.min)):
    """
    Returns the datetime of the form start_date + i * delta
    which is closest to dt for any non-negative integer i.
    Note that delta may be a datetime.timedelta or a dateutil.relativedelta
    >>> round_time(datetime(2015, 1, 1, 6), timedelta(days=1))
    datetime.datetime(2015, 1, 1, 0, 0)
    >>> round_time(datetime(2015, 1, 2), relativedelta(months=1))
    datetime.datetime(2015, 1, 1, 0, 0)
    >>> round_time(datetime(2015, 9, 16, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
    datetime.datetime(2015, 9, 16, 0, 0)
    >>> round_time(datetime(2015, 9, 15, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
    datetime.datetime(2015, 9, 15, 0, 0)
    >>> round_time(datetime(2015, 9, 14, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
    datetime.datetime(2015, 9, 14, 0, 0)
    >>> round_time(datetime(2015, 9, 13, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
    datetime.datetime(2015, 9, 14, 0, 0)
    """
    if isinstance(delta, six.string_types):
        tz = start_date.tzinfo
        start_date = timezone.make_naive(start_date, tz)
        cron = croniter(delta, start_date)
        prev = cron.get_prev(datetime)
        if prev == start_date:
            return timezone.make_aware(start_date, tz)
        else:
            return timezone.make_aware(prev, tz)
    dt -= timedelta(microseconds=(dt.microsecond))
    upper = 1
    while start_date + upper * delta < dt:
        upper *= 2

    lower = upper // 2
    while True:
        if start_date + (lower + 1) * delta >= dt:
            if start_date + (lower + 1) * delta - dt <= dt - (start_date + lower * delta):
                return start_date + (lower + 1) * delta
            else:
                return start_date + lower * delta
        candidate = lower + (upper - lower) // 2
        if start_date + candidate * delta >= dt:
            upper = candidate
        else:
            lower = candidate


def infer_time_unit(time_seconds_arr):
    """
    Determine the most appropriate time unit for an array of time durations
    specified in seconds.
    e.g. 5400 seconds => 'minutes', 36000 seconds => 'hours'
    """
    if len(time_seconds_arr) == 0:
        return 'hours'
    else:
        max_time_seconds = max(time_seconds_arr)
        if max_time_seconds <= 120:
            return 'seconds'
        if max_time_seconds <= 7200:
            return 'minutes'
        if max_time_seconds <= 172800:
            return 'hours'
        return 'days'


def scale_time_units(time_seconds_arr, unit):
    """
    Convert an array of time durations in seconds to the specified time unit.
    """
    if unit == 'minutes':
        return list(map(lambda x: x * 1.0 / 60, time_seconds_arr))
    else:
        if unit == 'hours':
            return list(map(lambda x: x * 1.0 / 3600, time_seconds_arr))
        if unit == 'days':
            return list(map(lambda x: x * 1.0 / 86400, time_seconds_arr))
        return time_seconds_arr


def days_ago(n, hour=0, minute=0, second=0, microsecond=0):
    """
    Get a datetime object representing `n` days ago. By default the time is
    set to midnight.
    """
    today = timezone.utcnow().replace(hour=hour,
      minute=minute,
      second=second,
      microsecond=microsecond)
    return today - timedelta(days=n)


def parse_execution_date(execution_date_str):
    """
    Parse execution date string to datetime object.
    """
    return timezone.parse(execution_date_str)