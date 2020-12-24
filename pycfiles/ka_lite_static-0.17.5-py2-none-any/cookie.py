# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/http/cookie.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import, unicode_literals
from django.utils.encoding import force_str
from django.utils import six
from django.utils.six.moves import http_cookies
_cookie_encodes_correctly = http_cookies.SimpleCookie().value_encode(b';') == (';',
                                                                               '"\\073"')
_tc = http_cookies.SimpleCookie()
try:
    _tc.load(str(b'foo:bar=1'))
    _cookie_allows_colon_in_names = True
except http_cookies.CookieError:
    _cookie_allows_colon_in_names = False

if _cookie_encodes_correctly and _cookie_allows_colon_in_names:
    SimpleCookie = http_cookies.SimpleCookie
else:
    Morsel = http_cookies.Morsel

    class SimpleCookie(http_cookies.SimpleCookie):
        if not _cookie_encodes_correctly:

            def value_encode(self, val):
                val, encoded = super(SimpleCookie, self).value_encode(val)
                encoded = encoded.replace(b';', b'\\073').replace(b',', b'\\054')
                if b'\\' in encoded and not encoded.startswith(b'"'):
                    encoded = b'"' + encoded + b'"'
                return (val, encoded)

        if not _cookie_allows_colon_in_names:

            def load(self, rawdata):
                self.bad_cookies = set()
                if not six.PY3 and isinstance(rawdata, six.text_type):
                    rawdata = force_str(rawdata)
                super(SimpleCookie, self).load(rawdata)
                for key in self.bad_cookies:
                    del self[key]

            def _BaseCookie__set(self, key, real_value, coded_value):
                key = force_str(key)
                try:
                    M = self.get(key, Morsel())
                    M.set(key, real_value, coded_value)
                    dict.__setitem__(self, key, M)
                except http_cookies.CookieError:
                    self.bad_cookies.add(key)
                    dict.__setitem__(self, key, http_cookies.Morsel())


def parse_cookie(cookie):
    if cookie == b'':
        return {}
    if not isinstance(cookie, http_cookies.BaseCookie):
        try:
            c = SimpleCookie()
            c.load(cookie)
        except http_cookies.CookieError:
            return {}

    else:
        c = cookie
    cookiedict = {}
    for key in c.keys():
        cookiedict[key] = c.get(key).value

    return cookiedict