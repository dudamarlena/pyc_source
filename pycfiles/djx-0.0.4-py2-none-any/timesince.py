# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/timesince.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import calendar, datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware, utc
from django.utils.translation import ugettext, ungettext_lazy
TIMESINCE_CHUNKS = (
 (
  31536000, ungettext_lazy(b'%d year', b'%d years')),
 (
  2592000, ungettext_lazy(b'%d month', b'%d months')),
 (
  604800, ungettext_lazy(b'%d week', b'%d weeks')),
 (
  86400, ungettext_lazy(b'%d day', b'%d days')),
 (
  3600, ungettext_lazy(b'%d hour', b'%d hours')),
 (
  60, ungettext_lazy(b'%d minute', b'%d minutes')))

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
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)
    if not now:
        now = datetime.datetime.now(utc if is_aware(d) else None)
    if reversed:
        d, now = now, d
    delta = now - d
    leapdays = calendar.leapdays(d.year, now.year)
    if leapdays != 0:
        if calendar.isleap(d.year):
            leapdays -= 1
        elif calendar.isleap(now.year):
            leapdays += 1
    delta -= datetime.timedelta(leapdays)
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        return avoid_wrapping(ugettext(b'0 minutes'))
    else:
        for i, (seconds, name) in enumerate(TIMESINCE_CHUNKS):
            count = since // seconds
            if count != 0:
                break

        result = avoid_wrapping(name % count)
        if i + 1 < len(TIMESINCE_CHUNKS):
            seconds2, name2 = TIMESINCE_CHUNKS[(i + 1)]
            count2 = (since - seconds * count) // seconds2
            if count2 != 0:
                result += ugettext(b', ') + avoid_wrapping(name2 % count2)
        return result


def timeuntil(d, now=None):
    """
    Like timesince, but returns a string measuring the time until
    the given time.
    """
    return timesince(d, now, reversed=True)