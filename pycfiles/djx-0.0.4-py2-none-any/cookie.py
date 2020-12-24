# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/http/cookie.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import sys
from django.utils import six
from django.utils.encoding import force_str
from django.utils.six.moves import http_cookies
_cookie_allows_colon_in_names = six.PY3
cookie_pickles_properly = sys.version_info[:2] == (2, 7) and sys.version_info >= (2,
                                                                                  7,
                                                                                  9) or sys.version_info >= (3,
                                                                                                             4,
                                                                                                             3)
if _cookie_allows_colon_in_names and cookie_pickles_properly:
    SimpleCookie = http_cookies.SimpleCookie
else:
    Morsel = http_cookies.Morsel

    class SimpleCookie(http_cookies.SimpleCookie):
        if not cookie_pickles_properly:

            def __setitem__(self, key, value):
                if isinstance(value, Morsel):
                    dict.__setitem__(self, key, value)
                else:
                    super(SimpleCookie, self).__setitem__(key, value)

        if not _cookie_allows_colon_in_names:

            def load(self, rawdata):
                self.bad_cookies = set()
                if isinstance(rawdata, six.text_type):
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
                    if not hasattr(self, b'bad_cookies'):
                        self.bad_cookies = set()
                    self.bad_cookies.add(key)
                    dict.__setitem__(self, key, http_cookies.Morsel())


def parse_cookie(cookie):
    """
    Return a dictionary parsed from a `Cookie:` header string.
    """
    cookiedict = {}
    if six.PY2:
        cookie = force_str(cookie)
    for chunk in cookie.split(str(b';')):
        if str(b'=') in chunk:
            key, val = chunk.split(str(b'='), 1)
        else:
            key, val = str(b''), chunk
        key, val = key.strip(), val.strip()
        if key or val:
            cookiedict[key] = http_cookies._unquote(val)

    return cookiedict