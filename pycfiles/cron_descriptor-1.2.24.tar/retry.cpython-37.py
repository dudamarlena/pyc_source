# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/util/retry.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 15450 bytes
from __future__ import absolute_import
import time, logging
from collections import namedtuple
from itertools import takewhile
import email, re
from ..exceptions import ConnectTimeoutError, MaxRetryError, ProtocolError, ReadTimeoutError, ResponseError, InvalidHeader
from ..packages import six
log = logging.getLogger(__name__)
RequestHistory = namedtuple('RequestHistory', ['method', 'url', 'error', 'status', 'redirect_location'])

class Retry(object):
    """Retry"""
    DEFAULT_METHOD_WHITELIST = frozenset([
     'HEAD', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'])
    RETRY_AFTER_STATUS_CODES = frozenset([413, 429, 503])
    DEFAULT_REDIRECT_HEADERS_BLACKLIST = frozenset(['Authorization'])
    BACKOFF_MAX = 120

    def __init__(self, total=10, connect=None, read=None, redirect=None, status=None, method_whitelist=DEFAULT_METHOD_WHITELIST, status_forcelist=None, backoff_factor=0, raise_on_redirect=True, raise_on_status=True, history=None, respect_retry_after_header=True, remove_headers_on_redirect=DEFAULT_REDIRECT_HEADERS_BLACKLIST):
        self.total = total
        self.connect = connect
        self.read = read
        self.status = status
        if redirect is False or total is False:
            redirect = 0
            raise_on_redirect = False
        self.redirect = redirect
        self.status_forcelist = status_forcelist or 
        self.method_whitelist = method_whitelist
        self.backoff_factor = backoff_factor
        self.raise_on_redirect = raise_on_redirect
        self.raise_on_status = raise_on_status
        self.history = history or 
        self.respect_retry_after_header = respect_retry_after_header
        self.remove_headers_on_redirect = frozenset([h.lower() for h in remove_headers_on_redirect])

    def new(self, **kw):
        params = dict(total=(self.total),
          connect=(self.connect),
          read=(self.read),
          redirect=(self.redirect),
          status=(self.status),
          method_whitelist=(self.method_whitelist),
          status_forcelist=(self.status_forcelist),
          backoff_factor=(self.backoff_factor),
          raise_on_redirect=(self.raise_on_redirect),
          raise_on_status=(self.raise_on_status),
          history=(self.history),
          remove_headers_on_redirect=(self.remove_headers_on_redirect),
          respect_retry_after_header=(self.respect_retry_after_header))
        params.update(kw)
        return (type(self))(**params)

    @classmethod
    def from_int(cls, retries, redirect=True, default=None):
        """ Backwards-compatibility for the old retries format."""
        if retries is None:
            retries = default if default is not None else cls.DEFAULT
        if isinstance(retries, Retry):
            return retries
        redirect = bool(redirect) and None
        new_retries = cls(retries, redirect=redirect)
        log.debug('Converted retries value: %r -> %r', retries, new_retries)
        return new_retries

    def get_backoff_time(self):
        """ Formula for computing the current backoff

        :rtype: float
        """
        consecutive_errors_len = len(list(takewhile(lambda x: x.redirect_location is None, reversed(self.history))))
        if consecutive_errors_len <= 1:
            return 0
        backoff_value = self.backoff_factor * 2 ** (consecutive_errors_len - 1)
        return min(self.BACKOFF_MAX, backoff_value)

    def parse_retry_after(self, retry_after):
        if re.match('^\\s*[0-9]+\\s*$', retry_after):
            seconds = int(retry_after)
        else:
            retry_date_tuple = email.utils.parsedate(retry_after)
            if retry_date_tuple is None:
                raise InvalidHeader('Invalid Retry-After header: %s' % retry_after)
            retry_date = time.mktime(retry_date_tuple)
            seconds = retry_date - time.time()
        if seconds < 0:
            seconds = 0
        return seconds

    def get_retry_after(self, response):
        """ Get the value of Retry-After in seconds. """
        retry_after = response.getheader('Retry-After')
        if retry_after is None:
            return
        return self.parse_retry_after(retry_after)

    def sleep_for_retry(self, response=None):
        retry_after = self.get_retry_after(response)
        if retry_after:
            time.sleep(retry_after)
            return True
        return False

    def _sleep_backoff(self):
        backoff = self.get_backoff_time()
        if backoff <= 0:
            return
        time.sleep(backoff)

    def sleep(self, response=None):
        """ Sleep between retry attempts.

        This method will respect a server's ``Retry-After`` response header
        and sleep the duration of the time requested. If that is not present, it
        will use an exponential backoff. By default, the backoff factor is 0 and
        this method will return immediately.
        """
        if self.respect_retry_after_header:
            if response:
                slept = self.sleep_for_retry(response)
                if slept:
                    return
        self._sleep_backoff()

    def _is_connection_error(self, err):
        """ Errors when we're fairly sure that the server did not receive the
        request, so it should be safe to retry.
        """
        return isinstance(err, ConnectTimeoutError)

    def _is_read_error(self, err):
        """ Errors that occur after the request has been started, so we should
        assume that the server began processing it.
        """
        return isinstance(err, (ReadTimeoutError, ProtocolError))

    def _is_method_retryable(self, method):
        """ Checks if a given HTTP method should be retried upon, depending if
        it is included on the method whitelist.
        """
        if self.method_whitelist:
            if method.upper() not in self.method_whitelist:
                return False
        return True

    def is_retry(self, method, status_code, has_retry_after=False):
        """ Is this method/status code retryable? (Based on whitelists and control
        variables such as the number of total retries to allow, whether to
        respect the Retry-After header, whether this header is present, and
        whether the returned status code is on the list of status codes to
        be retried upon on the presence of the aforementioned header)
        """
        if not self._is_method_retryable(method):
            return False
        if self.status_forcelist:
            if status_code in self.status_forcelist:
                return True
        return self.total and self.respect_retry_after_header and has_retry_after and status_code in self.RETRY_AFTER_STATUS_CODES

    def is_exhausted(self):
        """ Are we out of retries? """
        retry_counts = (
         self.total, self.connect, self.read, self.redirect, self.status)
        retry_counts = list(filter(None, retry_counts))
        if not retry_counts:
            return False
        return min(retry_counts) < 0

    def increment(self, method=None, url=None, response=None, error=None, _pool=None, _stacktrace=None):
        """ Return a new Retry object with incremented retry counters.

        :param response: A response object, or None, if the server did not
            return a response.
        :type response: :class:`~urllib3.response.HTTPResponse`
        :param Exception error: An error encountered during the request, or
            None if the response was received successfully.

        :return: A new ``Retry`` object.
        """
        if self.total is False:
            if error:
                raise six.reraise(type(error), error, _stacktrace)
        else:
            total = self.total
            if total is not None:
                total -= 1
            connect = self.connect
            read = self.read
            redirect = self.redirect
            status_count = self.status
            cause = 'unknown'
            status = None
            redirect_location = None
            if error:
                if self._is_connection_error(error):
                    if connect is False:
                        raise six.reraise(type(error), error, _stacktrace)
                elif connect is not None:
                    connect -= 1
            elif error and self._is_read_error(error):
                if not read is False:
                    if not self._is_method_retryable(method):
                        raise six.reraise(type(error), error, _stacktrace)
                elif read is not None:
                    read -= 1
            elif response and response.get_redirect_location():
                if redirect is not None:
                    redirect -= 1
                cause = 'too many redirects'
                redirect_location = response.get_redirect_location()
                status = response.status
            else:
                cause = ResponseError.GENERIC_ERROR
                if response:
                    if response.status:
                        if status_count is not None:
                            status_count -= 1
                        cause = ResponseError.SPECIFIC_ERROR.format(status_code=(response.status))
                        status = response.status
        history = self.history + (
         RequestHistory(method, url, error, status, redirect_location),)
        new_retry = self.new(total=total,
          connect=connect,
          read=read,
          redirect=redirect,
          status=status_count,
          history=history)
        if new_retry.is_exhausted():
            raise MaxRetryError(_pool, url, error or )
        log.debug("Incremented Retry for (url='%s'): %r", url, new_retry)
        return new_retry

    def __repr__(self):
        return '{cls.__name__}(total={self.total}, connect={self.connect}, read={self.read}, redirect={self.redirect}, status={self.status})'.format(cls=(type(self)),
          self=self)


Retry.DEFAULT = Retry(3)