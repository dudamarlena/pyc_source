# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/throttle.py
# Compiled at: 2018-08-13 08:58:37
"""
Utility module for throttling calls to a function
"""
import collections, datetime, logging, time
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Throttle(object):
    """
    Limits the number of calls to a function to a given rate.

    The rate limit is equal to the max_calls over the interval_in_seconds.

    :param function: function to call after throttling
    :param max_calls: maximum number of calls allowed
    :param interval_in_seconds: size of the sliding window
    """

    def __init__(self, function, max_calls, interval_in_seconds=60):
        assert max_calls > 0
        assert interval_in_seconds > 0
        self._actual = function
        self._max_requests = max_calls
        self._interval = datetime.timedelta(seconds=interval_in_seconds)
        self._timestamps = collections.deque(maxlen=self._max_requests)

    def __call__(self, *args, **kwargs):
        """ Conditionally delays before calling the function """
        self._wait()
        return self._actual(*args, **kwargs)

    def _limit_reached(self):
        """ Returns True if the maximum number of calls has been reached """
        return len(self._timestamps) == self._max_requests

    @staticmethod
    def _now():
        return datetime.datetime.now()

    def _remove_old_entries(self):
        """ Removes old timestamp entries """
        while len(self._timestamps) > 0 and self._now() - self._timestamps[0] >= self._interval:
            self._timestamps.popleft()

    @staticmethod
    def _sleep(seconds):
        return time.sleep(seconds)

    def _wait(self):
        """ Sleeps for the remaining interval if the limit has been reached """
        if self._limit_reached():
            logger.warn(('Throttling limit {} reached.').format(self._max_requests))
            lapsed = self._now() - self._timestamps[0]
            if lapsed < self._interval:
                sleep_time = (self._interval - lapsed).total_seconds()
                logger.debug(('Sleeping for {} seconds to prevent too many calls').format(sleep_time))
                self._sleep(sleep_time)
            self._remove_old_entries()
        self._timestamps.append(self._now())