# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/retry.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 5671 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import next
from contextlib import contextmanager
import time, urllib.request, urllib.error, urllib.parse
try:
    from httplib import BadStatusLine
except ImportError:
    from http.client import BadStatusLine

import logging
log = logging.getLogger(__name__)

def never(exception):
    return False


def retry(delays=(0, 1, 1, 4, 16, 64), timeout=300, predicate=never):
    """
    Retry an operation while the failure matches a given predicate and until a given timeout
    expires, waiting a given amount of time in between attempts. This function is a generator
    that yields contextmanagers. See doctests below for example usage.

    :param Iterable[float] delays: an interable yielding the time in seconds to wait before each
           retried attempt, the last element of the iterable will be repeated.

    :param float timeout: a overall timeout that should not be exceeded for all attempts together.
           This is a best-effort mechanism only and it won't abort an ongoing attempt, even if the
           timeout expires during that attempt.

    :param Callable[[Exception],bool] predicate: a unary callable returning True if another
           attempt should be made to recover from the given exception. The default value for this
           parameter will prevent any retries!

    :return: a generator yielding context managers, one per attempt
    :rtype: Iterator

    Retry for a limited amount of time:

    >>> true = lambda _:True
    >>> false = lambda _:False
    >>> i = 0
    >>> for attempt in retry( delays=[0], timeout=.1, predicate=true ):
    ...     with attempt:
    ...         i += 1
    ...         raise RuntimeError('foo')
    Traceback (most recent call last):
    ...
    RuntimeError: foo
    >>> i > 1
    True

    If timeout is 0, do exactly one attempt:

    >>> i = 0
    >>> for attempt in retry( timeout=0 ):
    ...     with attempt:
    ...         i += 1
    ...         raise RuntimeError( 'foo' )
    Traceback (most recent call last):
    ...
    RuntimeError: foo
    >>> i
    1

    Don't retry on success:

    >>> i = 0
    >>> for attempt in retry( delays=[0], timeout=.1, predicate=true ):
    ...     with attempt:
    ...         i += 1
    >>> i
    1

    Don't retry on unless predicate returns True:

    >>> i = 0
    >>> for attempt in retry( delays=[0], timeout=.1, predicate=false):
    ...     with attempt:
    ...         i += 1
    ...         raise RuntimeError( 'foo' )
    Traceback (most recent call last):
    ...
    RuntimeError: foo
    >>> i
    1
    """
    if timeout > 0:
        go = [
         None]

        @contextmanager
        def repeated_attempt(delay):
            try:
                yield
            except Exception as e:
                if time.time() + delay < expiration:
                    if predicate(e):
                        log.info('Got %s, trying again in %is.', e, delay)
                        time.sleep(delay)
                else:
                    raise
            else:
                go.pop()

        delays = iter(delays)
        expiration = time.time() + timeout
        delay = next(delays)
        while go:
            yield repeated_attempt(delay)
            delay = next(delays, delay)

    else:

        @contextmanager
        def single_attempt():
            yield

        yield single_attempt()


default_delays = (0, 1, 1, 4, 16, 64)
default_timeout = 300

def retryable_http_error(e):
    """
    Determine if an error encountered during an HTTP download is likely to go away if we try again.
    """
    if isinstance(e, urllib.error.HTTPError):
        if e.code in ('503', '408', '500'):
            return True
    if isinstance(e, BadStatusLine):
        return True
    else:
        return False


def retry_http(delays=default_delays, timeout=default_timeout, predicate=retryable_http_error):
    """
    >>> i = 0
    >>> for attempt in retry_http(timeout=5):  # doctest: +IGNORE_EXCEPTION_DETAIL
    ...     with attempt:
    ...         i += 1
    ...         raise urllib.error.HTTPError('http://www.test.com', '408', 'some message', {}, None)
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 408: some message
    >>> i > 1
    True
    >>> i = 0
    >>> for attempt in retry_http(timeout=5):  # doctest: +IGNORE_EXCEPTION_DETAIL
    ...     with attempt:
    ...         i += 1
    ...         raise BadStatusLine('sad-cloud.gif')
    Traceback (most recent call last):
    ...
    BadStatusLine: sad-cloud.gif
    >>> i > 1
    True
    """
    return retry(delays=delays, timeout=timeout, predicate=predicate)