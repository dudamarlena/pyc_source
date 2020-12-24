# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/timestamp.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import, division
import datetime, time
from six import integer_types
from ipv8.util import old_round

class Timestamp(object):
    """Used for having a validated instance of a timestamp that we can easily compare."""

    def __init__(self, timestamp):
        """
        :param timestamp: Integer representation of a timestamp in milliseconds
        :type timestamp: integer_types
        :raises ValueError: Thrown when one of the arguments are invalid
        """
        super(Timestamp, self).__init__()
        if not isinstance(timestamp, integer_types):
            raise ValueError('Timestamp must be an integer')
        if timestamp < 0:
            raise ValueError('Timestamp can not be negative')
        self._timestamp = timestamp

    @classmethod
    def now(cls):
        """
        Create a timestamp with the time set to the current time

        :return: A timestamp
        :rtype: Timestamp
        """
        return cls(int(old_round(time.time() * 1000)))

    def __int__(self):
        return self._timestamp

    def __str__(self):
        return '%s' % datetime.datetime.fromtimestamp(self._timestamp // 1000)

    def __lt__(self, other):
        if isinstance(other, Timestamp):
            return self._timestamp < other._timestamp
        if isinstance(other, integer_types):
            return self._timestamp < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Timestamp):
            return self._timestamp <= other._timestamp
        if isinstance(other, integer_types):
            return self._timestamp <= other
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, Timestamp):
            return NotImplemented
        if self is other:
            return True
        return self._timestamp == other._timestamp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, Timestamp):
            return self._timestamp > other._timestamp
        if isinstance(other, integer_types):
            return self._timestamp > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Timestamp):
            return self._timestamp >= other._timestamp
        if isinstance(other, integer_types):
            return self._timestamp >= other
        return NotImplemented

    def __hash__(self):
        return hash(self._timestamp)