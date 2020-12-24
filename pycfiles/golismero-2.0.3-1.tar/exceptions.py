# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests/packages/urllib3/exceptions.py
# Compiled at: 2013-08-26 10:52:44


class HTTPError(Exception):
    """Base exception used by this module."""
    pass


class PoolError(HTTPError):
    """Base exception for errors caused within a pool."""

    def __init__(self, pool, message):
        self.pool = pool
        HTTPError.__init__(self, '%s: %s' % (pool, message))

    def __reduce__(self):
        return (
         self.__class__, (None, None))


class RequestError(PoolError):
    """Base exception for PoolErrors that have associated URLs."""

    def __init__(self, pool, url, message):
        self.url = url
        PoolError.__init__(self, pool, message)

    def __reduce__(self):
        return (
         self.__class__, (None, self.url, None))


class SSLError(HTTPError):
    """Raised when SSL certificate fails in an HTTPS connection."""
    pass


class DecodeError(HTTPError):
    """Raised when automatic decoding based on Content-Type fails."""
    pass


class MaxRetryError(RequestError):
    """Raised when the maximum number of retries is exceeded."""

    def __init__(self, pool, url, reason=None):
        self.reason = reason
        message = 'Max retries exceeded with url: %s' % url
        if reason:
            message += ' (Caused by %s: %s)' % (type(reason), reason)
        else:
            message += ' (Caused by redirect)'
        RequestError.__init__(self, pool, url, message)


class HostChangedError(RequestError):
    """Raised when an existing pool gets a request for a foreign host."""

    def __init__(self, pool, url, retries=3):
        message = 'Tried to open a foreign host with url: %s' % url
        RequestError.__init__(self, pool, url, message)
        self.retries = retries


class TimeoutError(RequestError):
    """Raised when a socket timeout occurs."""
    pass


class EmptyPoolError(PoolError):
    """Raised when a pool runs out of connections and no more are allowed."""
    pass


class ClosedPoolError(PoolError):
    """Raised when a request enters a pool after the pool has been closed."""
    pass


class LocationParseError(ValueError, HTTPError):
    """Raised when get_host or similar fails to parse the URL input."""

    def __init__(self, location):
        message = 'Failed to parse: %s' % location
        HTTPError.__init__(self, message)
        self.location = location