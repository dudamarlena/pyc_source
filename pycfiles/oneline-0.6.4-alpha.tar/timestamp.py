# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/timestamp.py
# Compiled at: 2014-07-29 17:29:28
"""Tools for representing MongoDB internal Timestamps.
"""
import calendar, datetime
from bson.tz_util import utc
UPPERBOUND = 4294967296

class Timestamp(object):
    """MongoDB internal timestamps used in the opLog.
    """
    _type_marker = 17

    def __init__(self, time, inc):
        """Create a new :class:`Timestamp`.

        This class is only for use with the MongoDB opLog. If you need
        to store a regular timestamp, please use a
        :class:`~datetime.datetime`.

        Raises :class:`TypeError` if `time` is not an instance of
        :class: `int` or :class:`~datetime.datetime`, or `inc` is not
        an instance of :class:`int`. Raises :class:`ValueError` if
        `time` or `inc` is not in [0, 2**32).

        :Parameters:
          - `time`: time in seconds since epoch UTC, or a naive UTC
            :class:`~datetime.datetime`, or an aware
            :class:`~datetime.datetime`
          - `inc`: the incrementing counter

        .. versionchanged:: 1.7
           `time` can now be a :class:`~datetime.datetime` instance.
        """
        if isinstance(time, datetime.datetime):
            if time.utcoffset() is not None:
                time = time - time.utcoffset()
            time = int(calendar.timegm(time.timetuple()))
        if not isinstance(time, (int, long)):
            raise TypeError('time must be an instance of int')
        if not isinstance(inc, (int, long)):
            raise TypeError('inc must be an instance of int')
        if not 0 <= time < UPPERBOUND:
            raise ValueError('time must be contained in [0, 2**32)')
        if not 0 <= inc < UPPERBOUND:
            raise ValueError('inc must be contained in [0, 2**32)')
        self.__time = time
        self.__inc = inc
        return

    @property
    def time(self):
        """Get the time portion of this :class:`Timestamp`.
        """
        return self.__time

    @property
    def inc(self):
        """Get the inc portion of this :class:`Timestamp`.
        """
        return self.__inc

    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.__time == other.time and self.__inc == other.inc
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, Timestamp):
            return (self.time, self.inc) < (other.time, other.inc)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Timestamp):
            return (self.time, self.inc) <= (other.time, other.inc)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Timestamp):
            return (self.time, self.inc) > (other.time, other.inc)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Timestamp):
            return (self.time, self.inc) >= (other.time, other.inc)
        return NotImplemented

    def __repr__(self):
        return 'Timestamp(%s, %s)' % (self.__time, self.__inc)

    def as_datetime(self):
        """Return a :class:`~datetime.datetime` instance corresponding
        to the time portion of this :class:`Timestamp`.

        .. versionchanged:: 1.8
           The returned datetime is now timezone aware.
        """
        return datetime.datetime.fromtimestamp(self.__time, utc)