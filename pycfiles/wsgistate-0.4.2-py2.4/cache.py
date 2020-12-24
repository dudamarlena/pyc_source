# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/cache.py
# Compiled at: 2007-10-22 19:32:44
"""WSGI middleware for caching."""
import time, rfc822
from StringIO import StringIO
__all__ = [
 'WsgiMemoize', 'CacheHeader', 'memoize', 'public', 'private', 'nocache', 'nostore', 'notransform', 'revalidate', 'proxyrevalidate', 'maxage', 'smaxage', 'vary', 'modified']

def memoize(cache, **kw):
    """Decorator for caching."""

    def decorator(application):
        return WsgiMemoize(application, cache, **kw)

    return decorator


def getinput(environ):
    """Non-destructively retrieves wsgi.input value."""
    wsginput = environ['wsgi.input']
    if hasattr(wsginput, 'getvalue'):
        qs = wsginput.getvalue()
    else:
        clength = int(environ['CONTENT_LENGTH'])
        qs = wsginput.read(clength)
        environ['wsgi.input'] = StringIO(qs)
    return qs


def expiredate(seconds, value):
    """Expire date headers for cache control.

    @param seconds Seconds
    @param value Value for Cache-Control header
    """
    now = time.time()
    return {'Cache-Control': value % seconds, 'Date': rfc822.formatdate(now), 'Expires': rfc822.formatdate(now + seconds)}


def control(application, value):
    """Generic setter for 'Cache-Control' headers.

    @param application WSGI application
    @param value 'Cache-Control' value
    """
    headers = {'Cache-Control': value}
    return CacheHeader(application, headers)


def expire(application, value):
    """Generic setter for 'Cache-Control' headers + expiration info.

    @param application WSGI application
    @param value 'Cache-Control' value
    """
    now = rfc822.formatdate()
    headers = {'Cache-Control': value, 'Date': now, 'Expires': now}
    return CacheHeader(application, headers)


def age(value, second):
    """Generic setter for 'Cache-Control' headers + future expiration info.

    @param value 'Cache-Control' value
    @param seconds # of seconds a resource should be considered invalid in
    """

    def decorator(application):
        return CacheHeader(application, expiredate(second, value))

    return decorator


def public(application):
    """Response MAY be cached."""
    return control(application, 'public')


def private(application):
    """Response intended for 1 user that MUST NOT be cached."""
    return expire(application, 'private')


def nocache(application):
    """Response that a cache can't send without origin server revalidation."""
    now = rfc822.formatdate()
    headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Date': now, 'Expires': now}
    return CacheHeader(application, headers)


def nostore(application):
    """Response that MUST NOT be cached."""
    return expire(application, 'no-store')


def notransform(application):
    """A cache must not modify the Content-Location, Content-MD5, ETag,
    Last-Modified, Expires, Content-Encoding, Content-Range, and Content-Type
    headers.
    """
    return control(application, 'no-transform')


def revalidate(application):
    """A cache must revalidate a response with the origin server."""
    return control(application, 'must-revalidate')


def proxyrevalidate(application):
    """Shared caches must revalidate a response with the origin server."""
    return control(application, 'proxy-revalidate')


def maxage(seconds):
    """Sets the maximum time in seconds a response can be cached."""
    return age('max-age=%d', seconds)


def smaxage(seconds):
    """Sets the maximum time in seconds a shared cache can store a response."""
    return age('s-maxage=%d', seconds)


def expires(seconds):
    """Sets the time a response expires from the cache (HTTP 1.0)."""
    headers = {'Expires': rfc822.formatdate(time.time() + seconds)}

    def decorator(application):
        return CacheHeader(application, headers)

    return decorator


def vary(headers):
    """Sets which fields allow a cache to use a response without revalidation."""
    headers = {'Vary': (', ').join(headers)}

    def decorator(application):
        return CacheHeader(application, headers)

    return decorator


def modified(seconds=None):
    """Sets the time a response was modified."""
    headers = {'Modified': rfc822.formatdate(seconds)}

    def decorator(application):
        return CacheHeader(application, headers)

    return decorator


class CacheHeader(object):
    """Controls HTTP Cache Control headers."""
    __module__ = __name__

    def __init__(self, application, headers):
        self.application = application
        self.headers = headers

    def __call__(self, environ, start_response):
        if environ.get('REQUEST_METHOD') in ('GET', 'HEAD'):

            def hdr_response(status, headers, exc_info=None):
                theaders = self.headers.copy()
                if 'Cache-Control' in theaders:
                    for (idx, i) in enumerate(headers):
                        if i[0] != 'Cache-Control':
                            continue
                        curval = theaders.pop('Cache-Control')
                        newval = (', ').join([curval, i[1]])
                        headers.append(('Cache-Control', newval))
                        del headers[idx]
                        break

                headers.extend(((k, v) for (k, v) in theaders.iteritems()))
                return start_response(status, headers, exc_info)

            return self.application(environ, hdr_response)
        return self.application(environ, start_response)


class WsgiMemoize(object):
    """WSGI middleware for response memoizing."""
    __module__ = __name__

    def __init__(self, app, cache, **kw):
        self.application, self._cache = app, cache
        self._methkey = kw.get('key_methods', False)
        self._userkey = kw.get('key_user_info', False)
        self._allowed = kw.get('allowed_methods', set(['GET', 'HEAD']))

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] not in self._allowed:
            return self.application(environ, start_response)
        key = self._keygen(environ)
        info = self._cache.get(key)
        if info is not None:
            start_response(info['status'], info['headers'], info['exc_info'])
            return info['data']

        def cache_response(status, headers, exc_info=None):
            newhdrs = expiredate(self._cache.timeout, 's-maxage=%d')
            headers.extend(((k, v) for (k, v) in newhdrs.iteritems()))
            cachedict = {'status': status, 'headers': headers, 'exc_info': exc_info}
            self._cache.set(key, cachedict)
            return start_response(status, headers, exc_info)

        data = list(self.application(environ, cache_response))
        info = self._cache.get(key)
        info['data'] = data
        self._cache.set(key, info)
        return data

    def _keygen(self, environ):
        """Generates cache keys."""
        key = [
         environ['PATH_INFO']]
        if self._methkey:
            key.append(environ['REQUEST_METHOD'])
        if self._userkey:
            qs = environ.get('QUERY_STRING', '')
            if qs != '':
                key.append(qs)
            else:
                win = getinput(environ)
                if win != '':
                    key.append(win)
        return ('').join(key)