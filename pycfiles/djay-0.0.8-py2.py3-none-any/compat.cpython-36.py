# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/compat.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 1513 bytes
"""Compatibility module for Python 2 and 3 support."""
import sys
try:
    from urllib.parse import quote as urlquote
except ImportError:
    from urllib import quote as urlquote

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

__all__ = ('to_bytes', 'to_str', 'urlquote', 'urlencode')
PY3 = (3, 0) <= sys.version_info < (4, 0)
PY2 = (2, 6) <= sys.version_info < (2, 8)
if PY3:
    unicode = str

def to_str(b, encoding='utf-8'):
    """Ensure that b is text in the specified encoding."""
    if hasattr(b, 'decode'):
        if not isinstance(b, unicode):
            b = b.decode(encoding)
    return b


def to_bytes(s, encoding='utf-8'):
    """Ensure that s is converted to bytes from the encoding."""
    if hasattr(s, 'encode'):
        if not isinstance(s, bytes):
            s = s.encode(encoding)
    return s