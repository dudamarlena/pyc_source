# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ago.py
# Compiled at: 2018-10-06 15:02:30
from datetime import datetime, timedelta
units = ('year', 'day', 'hour', 'minute', 'second', 'millisecond', 'microsecond')

def get_delta_from_subject(subject):
    """Convert the subject to a timedelta and return it."""
    if isinstance(subject, timedelta):
        return subject
    if isinstance(subject, datetime):
        dt = subject
    else:
        try:
            subject = float(subject)
        except ValueError:
            raise TypeError('Unsupported subject type')

        dt = datetime.fromtimestamp(subject)
    return datetime.now(tz=dt.tzinfo) - dt


def delta2dict(delta):
    """Accepts a delta, returns a dictionary of units"""
    delta = abs(delta)
    return {'year': int(delta.days / 365), 
       'day': int(delta.days % 365), 
       'hour': int(delta.seconds / 3600), 
       'minute': int(delta.seconds / 60) % 60, 
       'second': delta.seconds % 60, 
       'millisecond': delta.microseconds / 1000, 
       'microsecond': delta.microseconds % 1000}


def human(subject, precision=2, past_tense='{} ago', future_tense='in {}', abbreviate=False):
    """
    Accept a subject, return a human readable timedelta string.

    :param subject: a datetime, timedelta, or timestamp (integer / float) object
    :param precision: the desired amount of unit precision (default: 2)
    :param past_tense: the format string used for a past timedelta (default: '{} ago')
    :param future_tense: the format string used for a future timedelta (default: 'in {}')
    :param abbreviate: boolean to abbreviate units (default: False)

    :returns: Human readable timedelta string (Str)
    """
    delta = get_delta_from_subject(subject)
    the_tense = future_tense if delta < timedelta(0) else past_tense
    d = delta2dict(delta)
    hlist = []
    count = 0
    for unit in units:
        if count >= precision:
            break
        if d[unit] == 0:
            continue
        if abbreviate:
            if unit == 'millisecond':
                abr = 'ms'
            elif unit == 'microsecond':
                abr = 'um'
            else:
                abr = unit[0]
            hlist.append(('{}{}').format(d[unit], abr))
        else:
            s = '' if d[unit] == 1 else 's'
            hlist.append(('{} {}{}').format(d[unit], unit, s))
        count += 1

    return the_tense.format((', ').join(hlist))