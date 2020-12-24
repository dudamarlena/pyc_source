# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/requests/compat.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = '\npythoncompat\n'
from .packages import chardet
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
try:
    import simplejson as json
except (ImportError, SyntaxError):
    import json

if is_py2:
    from urllib import quote, unquote, quote_plus, unquote_plus, urlencode, getproxies, proxy_bypass
    from urlparse import urlparse, urlunparse, urljoin, urlsplit, urldefrag
    from urllib2 import parse_http_list
    import cookielib
    from Cookie import Morsel
    from StringIO import StringIO
    from .packages.urllib3.packages.ordered_dict import OrderedDict
    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)
elif is_py3:
    from urllib.parse import urlparse, urlunparse, urljoin, urlsplit, urlencode, quote, unquote, quote_plus, unquote_plus, urldefrag
    from urllib.request import parse_http_list, getproxies, proxy_bypass
    from http import cookiejar as cookielib
    from http.cookies import Morsel
    from io import StringIO
    from collections import OrderedDict
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)