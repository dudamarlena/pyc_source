# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/urllib/parse.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 1053 bytes
from __future__ import absolute_import
from future.standard_library import suspend_hooks
from future.utils import PY3
if PY3:
    from urllib.parse import *
else:
    __future_module__ = True
    from urlparse import ParseResult, SplitResult, parse_qs, parse_qsl, urldefrag, urljoin, urlparse, urlsplit, urlunparse, urlunsplit
    with suspend_hooks():
        from urllib import quote, quote_plus, unquote, unquote_plus, urlencode, splitquery