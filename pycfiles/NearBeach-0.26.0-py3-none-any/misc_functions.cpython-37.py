# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/misc_functions.py
# Compiled at: 2019-11-08 17:24:24
# Size of source mod 2**32: 2920 bytes
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from django.utils import timezone
from django.conf import settings
import datetime, pytz
from collections import namedtuple

def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dictfetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def convert_extracted_time(datetime):
    """
    NearBeach stores its time in UTC. This function is designed to get the UTC time and convert it into
    the correct timezone, and from there it then converts the time into a dictionary model (hour, minutes, AM/PM)
    and returns that.
    :param datetime: this will be the datetime extract from the model
    :return: { 'hour': hour, 'minute': minute, 'meridiem': meridiem }
    """
    datetime = datetime.replace(tzinfo=(pytz.utc))
    datetime_converted = datetime.astimezone(pytz.timezone(settings.TIME_ZONE))
    year = datetime_converted.year
    month = datetime_converted.month
    day = datetime_converted.day
    hour = datetime_converted.hour
    minute = datetime_converted.minute
    meridiem = 'AM'
    if hour == 0:
        hour = 12
    else:
        if hour == 12:
            meridiem = 'PM'
        else:
            if hour > 12:
                hour = hour - 12
                meridiem = 'PM'
    return {'year':year,  'month':month, 
     'day':day, 
     'hour':hour, 
     'minute':minute, 
     'meridiem':meridiem}


def convert_to_utc(year, month, day, hour, minute, meridiem):
    """
    The data from the form is inputted into this function. The time is then converted into UTC from the local timezone.
    From there the datetime of the UTC is returned for input into the database.
    :param datetime:
    :return:
    """
    if meridiem == 'AM':
        if hour == 12:
            hour = 0
    elif hour < 12:
        hour = hour + 12
    location = pytz.timezone(settings.TIME_ZONE)
    local_time = location.localize(datetime.datetime(year, month, day, hour, minute))
    return local_time.astimezone(pytz.utc)