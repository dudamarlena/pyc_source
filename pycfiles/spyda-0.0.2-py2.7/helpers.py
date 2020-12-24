# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/tests/helpers.py
# Compiled at: 2013-03-25 21:23:33
try:
    from urllib.error import HTTPError, URLError
    from urllib.parse import quote, urlencode, urljoin
    from urllib.request import HTTPBasicAuthHandler, HTTPCookieProcessor
    from urllib.request import urlopen, build_opener, install_opener
    from urllib.request import HTTPDigestAuthHandler, Request
except ImportError:
    from urlparse import urljoin
    from urllib import quote, urlencode
    from urllib2 import HTTPError, URLError, HTTPDigestAuthHandler
    from urllib2 import HTTPBasicAuthHandler, HTTPCookieProcessor
    from urllib2 import urlopen, build_opener, install_opener, Request

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse