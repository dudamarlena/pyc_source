# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smorin/Dropbox/code/dedup/filegardener/test_data/1dup/seconddir/requests/exceptions.py
# Compiled at: 2016-07-21 23:59:52
"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.

"""
from .packages.urllib3.exceptions import HTTPError as BaseHTTPError

class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request."""

    def __init__(self, *args, **kwargs):
        """
        Initialize RequestException with `request` and `response` objects.
        """
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if response is not None and not self.request and hasattr(response, 'request'):
            self.request = self.response.request
        super(RequestException, self).__init__(*args, **kwargs)
        return


class HTTPError(RequestException):
    """An HTTP error occurred."""
    pass


class ConnectionError(RequestException):
    """A Connection error occurred."""
    pass


class ProxyError(ConnectionError):
    """A proxy error occurred."""
    pass


class SSLError(ConnectionError):
    """An SSL error occurred."""
    pass


class Timeout(RequestException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.
    """
    pass


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to connect to the remote server.

    Requests that produced this error are safe to retry.
    """
    pass


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""
    pass


class URLRequired(RequestException):
    """A valid URL is required to make a request."""
    pass


class TooManyRedirects(RequestException):
    """Too many redirects."""
    pass


class MissingSchema(RequestException, ValueError):
    """The URL schema (e.g. http or https) is missing."""
    pass


class InvalidSchema(RequestException, ValueError):
    """See defaults.py for valid schemas."""
    pass


class InvalidURL(RequestException, ValueError):
    """The URL provided was somehow invalid."""
    pass


class InvalidHeader(RequestException, ValueError):
    """The header value provided was somehow invalid."""
    pass


class ChunkedEncodingError(RequestException):
    """The server declared chunked encoding but sent an invalid chunk."""
    pass


class ContentDecodingError(RequestException, BaseHTTPError):
    """Failed to decode response content"""
    pass


class StreamConsumedError(RequestException, TypeError):
    """The content for this response was already consumed"""
    pass


class RetryError(RequestException):
    """Custom retries logic failed"""
    pass


class RequestsWarning(Warning):
    """Base warning for Requests."""
    pass


class FileModeWarning(RequestsWarning, DeprecationWarning):
    """
    A file was opened in text mode, but Requests determined its binary length.
    """
    pass