# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrew/hello/freebase/api/cookie_handlers.py
# Compiled at: 2009-06-18 13:50:01
import re
try:
    from google.appengine.api import urlfetch
    Http = object
except ImportError:
    pass

try:
    from httplib2 import Http
except ImportError:
    pass

try:
    import urllib
except ImportError:
    import urllib_stub as urllib

import cookielib

class DummyRequest(object):
    """Simulated urllib2.Request object for httplib2

       implements only what's necessary for cookielib.CookieJar to work
    """

    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        self.origin_req_host = cookielib.request_host(self)
        (self.type, r) = urllib.splittype(url)
        (self.host, r) = urllib.splithost(r)
        if self.host:
            self.host = urllib.unquote(self.host)

    def get_full_url(self):
        return self.url

    def get_origin_req_host(self):
        return self.origin_req_host

    def get_type(self):
        return self.type

    def get_host(self):
        return self.host

    def get_header(self, key, default=None):
        return self.headers.get(key.lower(), default)

    def has_header(self, key):
        return key in self.headers

    def add_unredirected_header(self, key, val):
        self.headers[key.lower()] = val

    def is_unverifiable(self):
        return False


class DummyHttplib2Response(object):
    """Simulated urllib2.Request object for httplib2

       implements only what's necessary for cookielib.CookieJar to work
    """

    def __init__(self, response):
        self.response = response

    def info(self):
        return DummyHttplib2Message(self.response)


class DummyUrlfetchResponse(object):
    """Simulated urllib2.Request object for httplib2

       implements only what's necessary for cookielib.CookieJar to work
    """

    def __init__(self, response):
        self.response = response

    def info(self):
        return DummyUrlfetchMessage(self.response)


class DummyHttplib2Message(object):
    """Simulated mimetools.Message object for httplib2

       implements only what's necessary for cookielib.CookieJar to work
    """

    def __init__(self, response):
        self.response = response

    def getheaders(self, k):
        k = k.lower()
        v = self.response.get(k.lower(), None)
        if k not in self.response:
            return []
        HEADERVAL = re.compile('\\s*(([^,]|(,\\s*\\d))+)')
        return [ h[0] for h in HEADERVAL.findall(self.response[k]) ]


class DummyUrlfetchMessage(object):
    """Simulated mimetools.Message object for httplib2

       implements only what's necessary for cookielib.CookieJar to work
    """

    def __init__(self, response):
        self.response = response

    def getheaders(self, k):
        k = k.lower()
        v = self.response.headers.get(k.lower(), None)
        if k not in self.response.headers:
            return []
        HEADERVAL = re.compile('\\s*(([^,]|(,\\s*\\d))+)')
        return [ h[0] for h in HEADERVAL.findall(self.response.headers[k]) ]


class CookiefulHttp(Http):
    """Subclass of httplib2.Http that keeps cookie state

       constructor takes an optional cookiejar=cookielib.CookieJar 

       currently this does not handle redirects completely correctly:
       if the server redirects to a different host the original
       cookies will still be sent to that host.
    """

    def __init__(self, cookiejar=None, **kws):
        Http.__init__(self, **kws)
        if cookiejar is None:
            cookiejar = cookielib.CookieJar()
        self.cookiejar = cookiejar
        return

    def request(self, uri, **kws):
        headers = kws.pop('headers', None)
        req = DummyRequest(uri, headers)
        self.cookiejar.add_cookie_header(req)
        headers = req.headers
        (r, body) = Http.request(self, uri, headers=headers, **kws)
        resp = DummyHttplib2Response(r)
        self.cookiejar.extract_cookies(resp, req)
        return (
         r, body)


class CookiefulUrlfetch(object):
    """Class that keeps cookie state

       constructor takes an optional cookiejar=cookielib.CookieJar
    """

    def __init__(self, cookiejar=None, **kws):
        if cookiejar is None:
            cookejar = cookielib.CookieJar()
        self.cookejar = cookiejar
        return

    def request(self, uri, **kws):
        headers = kws.pop('headers', None)
        req = DummyRequest(uri, headers)
        self.cookejar.add_cookie_header(req)
        headers = req.headers
        r = urlfetch.fetch(uri, headers=headers, **kws)
        self.cookejar.extract_cookies(DummyUrlfetchResponse(r), req)
        return r