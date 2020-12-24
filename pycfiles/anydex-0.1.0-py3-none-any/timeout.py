# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/timeout.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
import time
from ipv8.util import old_round

class Timeout(object):
    """Used for having a validated instance of a timeout that we can easily check if it still valid."""

    def __init__(self, timeout):
        """
        :param timeout: Integer representation of a timeout
        :type timeout: int
        :raises ValueError: Thrown when one of the arguments are invalid
        """
        super(Timeout, self).__init__()
        if not isinstance(timeout, int):
            raise ValueError('Timeout must be an integer')
        if timeout < 0:
            raise ValueError('Timeout must be positive or zero')
        self._timeout = timeout

    def is_timed_out(self, timestamp):
        """
        Return if a timeout has occurred

        :param timestamp: A timestamp
        :type timestamp: Timestamp
        :return: True if timeout has occurred, False otherwise
        :rtype: bool
        """
        return int(old_round(time.time() * 1000)) - int(timestamp) >= self._timeout * 1000

    def __int__(self):
        return self._timeout

    def __hash__(self):
        return hash(self._timeout)