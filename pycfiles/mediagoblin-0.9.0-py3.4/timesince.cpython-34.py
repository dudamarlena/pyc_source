# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/timesince.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3831 bytes
from __future__ import unicode_literals
import datetime, pytz
from mediagoblin.tools.translate import pass_to_ugettext, lazy_pass_to_ungettext as _

def timesince(d, now=None, reversed=False):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    chunks = (
     (
      31536000, lambda n: _('year', 'years', n)),
     (
      2592000, lambda n: _('month', 'months', n)),
     (
      604800, lambda n: _('week', 'weeks', n)),
     (
      86400, lambda n: _('day', 'days', n)),
     (
      3600, lambda n: _('hour', 'hours', n)),
     (
      60, lambda n: _('minute', 'minutes', n)))
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now:
        if not isinstance(now, datetime.datetime):
            now = datetime.datetime(now.year, now.month, now.day)
    if not now:
        now = datetime.datetime.utcnow()
    delta = d - now if reversed else now - d
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        return '0 ' + pass_to_ugettext('minutes')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break

    s = pass_to_ugettext('%(number)d %(type)s') % {'number': count,  'type': name(count)}
    if i + 1 < len(chunks):
        seconds2, name2 = chunks[(i + 1)]
        count2 = (since - seconds * count) // seconds2
        if count2 != 0:
            s += pass_to_ugettext(', %(number)d %(type)s') % {'number': count2,  'type': name2(count2)}
    return s