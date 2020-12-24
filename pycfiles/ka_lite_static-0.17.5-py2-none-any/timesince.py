# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/timesince.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import datetime
from django.utils.timezone import is_aware, utc
from django.utils.translation import ungettext, ugettext

def timesince(d, now=None, reversed=False):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from
    http://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    chunks = (
     (
      31536000, lambda n: ungettext(b'year', b'years', n)),
     (
      2592000, lambda n: ungettext(b'month', b'months', n)),
     (
      604800, lambda n: ungettext(b'week', b'weeks', n)),
     (
      86400, lambda n: ungettext(b'day', b'days', n)),
     (
      3600, lambda n: ungettext(b'hour', b'hours', n)),
     (
      60, lambda n: ungettext(b'minute', b'minutes', n)))
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)
    if not now:
        now = datetime.datetime.now(utc if is_aware(d) else None)
    delta = d - now if reversed else now - d
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        return b'0 ' + ugettext(b'minutes')
    else:
        for i, (seconds, name) in enumerate(chunks):
            count = since // seconds
            if count != 0:
                break

        s = ugettext(b'%(number)d %(type)s') % {b'number': count, b'type': name(count)}
        if i + 1 < len(chunks):
            seconds2, name2 = chunks[(i + 1)]
            count2 = (since - seconds * count) // seconds2
            if count2 != 0:
                s += ugettext(b', %(number)d %(type)s') % {b'number': count2, b'type': name2(count2)}
        return s


def timeuntil(d, now=None):
    """
    Like timesince, but returns a string measuring the time until
    the given time.
    """
    return timesince(d, now, reversed=True)