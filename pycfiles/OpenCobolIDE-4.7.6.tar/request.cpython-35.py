# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/urllib/request.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 3525 bytes
from __future__ import absolute_import
from future.standard_library import suspend_hooks
from future.utils import PY3
if PY3:
    from urllib.request import *
    from urllib.request import getproxies, pathname2url, proxy_bypass, quote, request_host, splitattr, splithost, splitpasswd, splitport, splitquery, splittag, splittype, splituser, splitvalue, thishost, to_bytes, unquote, unwrap, url2pathname, urlcleanup, urljoin, urlopen, urlparse, urlretrieve, urlsplit, urlunparse
else:
    __future_module__ = True
    with suspend_hooks():
        from urllib import *
        from urllib2 import *
        from urlparse import *
        from urllib import toBytes
        to_bytes = toBytes