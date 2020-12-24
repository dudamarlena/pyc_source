# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/retries.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import itertools, logging, random, time, functools
from django.utils.encoding import force_bytes
from sentry.utils import metrics
logger = logging.getLogger(__name__)

class RetryException(Exception):

    def __init__(self, message, exception):
        self.message = message
        self.exception = exception

    def __str__(self):
        return force_bytes(self.message, errors='replace')

    def __repr__(self):
        return ('<{}: {!r}>').format(type(self).__name__, self.message)


class RetryPolicy(object):

    def __call__(self, function):
        raise NotImplementedError

    @classmethod
    def wrap(cls, *args, **kwargs):
        """
        A decorator that may be used to wrap a function to be retried using
        this policy.
        """
        retrier = cls(*args, **kwargs)

        def decorator(fn):

            @functools.wraps(fn)
            def execute_with_retry(*args, **kwargs):
                return retrier(functools.partial(fn, *args, **kwargs))

            return execute_with_retry

        return decorator


class TimedRetryPolicy(RetryPolicy):
    """
    A time-based policy that can be used to retry a callable in the case of
    failure as many times as possible up to the ``timeout`` value (in seconds.)

    The ``delay`` function accepts one argument, a number which represents the
    number of this attempt (starting at 1.)
    """

    def __init__(self, timeout, delay=None, exceptions=(Exception,), metric_instance=None, metric_tags=None):
        if delay is None:

            def delay(i):
                return 0.1 + (random.random() - 0.5) / 10

        self.timeout = timeout
        self.delay = delay
        self.exceptions = exceptions
        self.clock = time
        self.metric_instance = metric_instance
        self.metric_tags = metric_tags or {}
        return

    def __call__(self, function):
        start = self.clock.time()
        try:
            for i in itertools.count(1):
                try:
                    return function()
                except self.exceptions as error:
                    delay = self.delay(i)
                    now = self.clock.time()
                    if now + delay > start + self.timeout:
                        raise RetryException('Could not successfully execute %r within %.3f seconds (%s attempts.)' % (
                         function, now - start, i), error)
                    else:
                        logger.debug('Failed to execute %r due to %r on attempt #%s, retrying in %s seconds...', function, error, i, delay)
                        self.clock.sleep(delay)

        finally:
            if self.metric_instance:
                metrics.timing('timedretrypolicy.duration', self.clock.time() - start, instance=self.metric_instance, tags=self.metric_tags)