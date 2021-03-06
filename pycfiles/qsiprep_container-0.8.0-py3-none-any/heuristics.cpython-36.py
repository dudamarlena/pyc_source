# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_vendor/cachecontrol/heuristics.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 4070 bytes
import calendar, time
from email.utils import formatdate, parsedate, parsedate_tz
from datetime import datetime, timedelta
TIME_FMT = '%a, %d %b %Y %H:%M:%S GMT'

def expire_after(delta, date=None):
    date = date or datetime.utcnow()
    return date + delta


def datetime_to_header(dt):
    return formatdate(calendar.timegm(dt.timetuple()))


class BaseHeuristic(object):

    def warning(self, response):
        """
        Return a valid 1xx warning header value describing the cache
        adjustments.

        The response is provided too allow warnings like 113
        http://tools.ietf.org/html/rfc7234#section-5.5.4 where we need
        to explicitly say response is over 24 hours old.
        """
        return '110 - "Response is Stale"'

    def update_headers(self, response):
        """Update the response headers with any new headers.

        NOTE: This SHOULD always include some Warning header to
              signify that the response was cached by the client, not
              by way of the provided headers.
        """
        return {}

    def apply(self, response):
        updated_headers = self.update_headers(response)
        if updated_headers:
            response.headers.update(updated_headers)
            warning_header_value = self.warning(response)
            if warning_header_value is not None:
                response.headers.update({'Warning': warning_header_value})
        return response


class OneDayCache(BaseHeuristic):
    __doc__ = '\n    Cache the response by providing an expires 1 day in the\n    future.\n    '

    def update_headers(self, response):
        headers = {}
        if 'expires' not in response.headers:
            date = parsedate(response.headers['date'])
            expires = expire_after(timedelta(days=1), date=datetime(*date[:6]))
            headers['expires'] = datetime_to_header(expires)
            headers['cache-control'] = 'public'
        return headers


class ExpiresAfter(BaseHeuristic):
    __doc__ = '\n    Cache **all** requests for a defined time period.\n    '

    def __init__(self, **kw):
        self.delta = timedelta(**kw)

    def update_headers(self, response):
        expires = expire_after(self.delta)
        return {'expires':datetime_to_header(expires),  'cache-control':'public'}

    def warning(self, response):
        tmpl = '110 - Automatically cached for %s. Response might be stale'
        return tmpl % self.delta


class LastModified(BaseHeuristic):
    __doc__ = '\n    If there is no Expires header already, fall back on Last-Modified\n    using the heuristic from\n    http://tools.ietf.org/html/rfc7234#section-4.2.2\n    to calculate a reasonable value.\n\n    Firefox also does something like this per\n    https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching_FAQ\n    http://lxr.mozilla.org/mozilla-release/source/netwerk/protocol/http/nsHttpResponseHead.cpp#397\n    Unlike mozilla we limit this to 24-hr.\n    '
    cacheable_by_default_statuses = {
     200, 203, 204, 206, 300, 301, 404, 405, 410, 414, 501}

    def update_headers(self, resp):
        headers = resp.headers
        if 'expires' in headers:
            return {}
        if 'cache-control' in headers:
            if headers['cache-control'] != 'public':
                return {}
        if resp.status not in self.cacheable_by_default_statuses:
            return {}
        if 'date' not in headers or 'last-modified' not in headers:
            return {}
        date = calendar.timegm(parsedate_tz(headers['date']))
        last_modified = parsedate(headers['last-modified'])
        if date is None or last_modified is None:
            return {}
        else:
            now = time.time()
            current_age = max(0, now - date)
            delta = date - calendar.timegm(last_modified)
            freshness_lifetime = max(0, min(delta / 10, 86400))
            if freshness_lifetime <= current_age:
                return {}
            expires = date + freshness_lifetime
            return {'expires': time.strftime(TIME_FMT, time.gmtime(expires))}

    def warning(self, resp):
        pass