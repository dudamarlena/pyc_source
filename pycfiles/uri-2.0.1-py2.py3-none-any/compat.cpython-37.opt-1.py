# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/compat.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 625 bytes
try:
    str = unicode
    py2 = True
except:
    str = str
    py2 = False

try:
    from html import escape
except ImportError:
    from cgi import escape

try:
    from urllib.parse import urljoin, urlsplit, quote_plus, unquote_plus
except ImportError:
    from urlparse import urljoin, urlsplit
    from urllib import quote_plus, unquote_plus

try:
    from pathlib import PurePosixPath as Path
except ImportError:
    from pathlib2 import PurePosixPath as Path

from re import compile as r
SENTINEL = object()