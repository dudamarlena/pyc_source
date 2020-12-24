# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/monkey.py
# Compiled at: 2019-12-24 12:23:23
from __future__ import absolute_import

def register_scheme(name):
    try:
        import urlparse
    except ImportError:
        from urllib import parse as urlparse

    uses = (
     urlparse.uses_netloc, urlparse.uses_query, urlparse.uses_relative, urlparse.uses_fragment)
    for use in uses:
        if name not in use:
            use.append(name)


register_scheme('app')
register_scheme('chrome-extension')

def patch_httprequest_repr():
    try:
        from django.http import HttpRequest
    except ImportError:
        return

    def safe_httprequest_repr(self):
        return '<%s: %s %r>' % (self.__class__.__name__, self.method, self.get_full_path())

    HttpRequest.__repr__ = safe_httprequest_repr


def patch_parse_cookie():
    try:
        from django.utils import six
        from django.utils.encoding import force_str
        from django.utils.six.moves import http_cookies
        from django import http
    except ImportError:
        return

    def safe_parse_cookie(cookie):
        """
        Return a dictionary parsed from a `Cookie:` header string.
        """
        cookiedict = {}
        if six.PY2:
            cookie = force_str(cookie)
        for chunk in cookie.split(';'):
            if '=' in chunk:
                key, val = chunk.split('=', 1)
            else:
                key, val = '', chunk
            key, val = key.strip(), val.strip()
            if key or val:
                cookiedict[key] = http_cookies._unquote(val)

        return cookiedict

    http.parse_cookie = safe_parse_cookie


def patch_django_views_debug():
    try:
        from django.views import debug
    except ImportError:
        return

    debug.get_safe_settings = lambda : {}


for patch in (patch_parse_cookie, patch_httprequest_repr, patch_django_views_debug):
    patch()