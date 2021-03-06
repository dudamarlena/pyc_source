# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/common/timeutil.py
# Compiled at: 2015-06-14 13:30:57
"""Time related utilities and helper functions."""
import functools, logging, datetime

class AfterDelta(object):
    """Decorator for controlling execution after period of time.

    .. py:decorator:: AfterDelta
        A decorator that has state and handles checking if period of time
        (delta) has passed before executing the function. That way if you
        need to control whether a piece of code executes in a loop, the delta
        is applied before execution otherwise NOOP
    """
    DEFAULT_DELTA = 60

    def __init__(self, method):
        self._method = method
        self.before = None
        return

    def get_delta(self):
        """Retrieves the delta (period of time to wait between executions)

        .. note::
            To change the delta simply subclass and override
            this one method, and use the subclass name as the decorator

        :returns:   period of time (seconds)
        :rtype:     int
        """
        return self.DEFAULT_DELTA

    def __call__(self, *args, **kwargs):
        if self.before is None:
            self.before = utcnow()
        if is_older_than(self.before, self.get_delta()):
            self.before = utcnow()
            return self._method(*args, **kwargs)
        else:
            return
            return


def timed(method=None, logger=None, loglvl=None):
    """Decorator for timing method or function.

    .. py:decorator:: timed(logger, loglvl)
        A decorator that times the execution of a method/function and logs
        using the supplied logger at the specified loglevel.

    :param method: the method being timed
    :param logging.Logger logger:   reference to logger
                                    (defaults to logger of module holding the
                                    decorated method or function)
    :param int loglvl:  a logging level from logging.LEVELS defaults to DEBUG
    """
    if method is None:
        return functools.partial(timed, logger=logger, loglvl=loglvl)
    else:
        if logger is None:
            logger = logging.getLogger(method.__module__)
        if loglvl is None or logging.getLevelName(loglvl).startswith('Level'):
            loglvl = logging.DEBUG

        @functools.wraps(method)
        def timer(*args, **kwargs):
            """Logs the execution time of the specified method.

        :param args: the positional inputs to the method being timed
        :param kwargs: the key-value inputs to the method being timed
        :return: output of method being timed
        """
            start = utcnow()
            result = method(*args, **kwargs)
            end = utcnow()
            logger.log(loglvl, '%s took %.4f secs', method.__name__, delta_seconds(start, end))
            return result

        return timer


def nvl_date(dt, default=None):
    """Determines if the provided date, time, or datetime has a value.

    Returns the provided value back or the value of default (current time)

    :param dt: an instance of a date, time, or datetime
    :param default: value to return if provided dt has no value
    :return: date, time, or datetime provided or default
    :rtype: datetime
    """
    _default = default if default else utcnow()
    if dt and isinstance(dt, datetime.datetime):
        return dt
    return _default


def utcnow():
    """Gets current time.

    :returns:   current time from utc
    :rtype:     datetime
    """
    return datetime.datetime.utcnow()


def time_delta_seconds(seconds):
    """Retrieves a timedelta

    :param int seconds: delta of seconds
    :returns:   timedelta by seconds
    :rtype:     timedelta
    """
    return datetime.timedelta(seconds=seconds)


def advance_time_delta(dt, timedelta):
    """Advances a datetime by a datetime.timedelta

    :param datetime dt: a specified date time
    :param datetime.timedelta timedelta:    time offset (delta)
    :returns:   a datetime incremented by delta
    :rtype:     datetime
    """
    return dt + timedelta


def advance_time_seconds(dt, seconds):
    """Advances a datetime by a seconds

    :param datetime dt: a specified date time
    :param int seconds: seconds (delta)
    :returns:   a datetime incremented by seconds
    :rtype:     datetime
    """
    return advance_time_delta(dt, time_delta_seconds(seconds))


def is_older_than(before, seconds):
    """Checks if a datetime is older than seconds

    :param datetime before: a datetime to check
    :param int seconds: seconds (delta)
    :returns:   True if before is older than seconds else False
    :rtype: bool
    """
    return utcnow() - before > time_delta_seconds(seconds)


def is_newer_than(after, seconds):
    """Checks if a datetime is newer than seconds

    :param datetime after: a datetime to check
    :param int seconds: seconds (delta)
    :returns:   True if before is newer than seconds else False
    :rtype: bool
    """
    return after - utcnow() > time_delta_seconds(seconds)


def delta_seconds(before, after):
    """Return the difference between two timing objects.

    Compute the difference in seconds between two date, time, or
    datetime objects (as a float, to microsecond resolution).

    :param before:  date, datetime, time object
    :param after:   date, datetime, time object
    :returns:       difference in seconds
    :rtype:         int
    """
    delta = after - before
    return total_seconds(delta)


def total_seconds(delta):
    """Return the total seconds of datetime.timedelta object.

    :param timedelta delta: a delta to convert
    :returns:   seconds
    :rtype:     int
    """
    return delta.total_seconds()


def is_soon(dt, window):
    """Determines if time is going to happen in the next window seconds.

    :param dt: the time
    :param window: minimum seconds to remain to consider the time not soon

    :return: True if expiration is within the given duration
    """
    soon = advance_time_seconds(utcnow(), window)
    return dt <= soon


ONE_WEEK = total_seconds(datetime.timedelta(weeks=1))