# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tele/show.py
# Compiled at: 2011-01-14 09:58:16
from __future__ import unicode_literals
from pytz import utc

class Show(object):
    """
    Represents a TV-show. On object construction the time is automatically
    convertet into UTC time and normalized.
    """

    def __init__(self, thetime, title, subtitle, genre):
        self.time = utc.normalize(thetime.astimezone(utc))
        self.title = title
        self.subtitle = subtitle
        self.genre = genre


class ShowList(list):
    """
    Is a ``list`` for TV shows with some convinience methods.
    """

    def get_at(self, thetime):
        """
        Returns the show running at the given time. If time is smaller than
        the first show's time a KeyError is raised. ``thetime`` is automatically
        converted into UTC time and normalized.
        """
        thetime = utc.normalize(thetime.astimezone(utc))
        shows = sorted(self, lambda a, b: cmp(a.time, b.time))
        if thetime < shows[0].time:
            raise KeyError(b'%s is before the first show' % thetime)
        lastshow = shows[0]
        for show in shows:
            if show.time > thetime:
                return lastshow
            lastshow = show

        return lastshow