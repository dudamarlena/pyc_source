# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/compat.py
# Compiled at: 2016-09-25 02:19:33
# Size of source mod 2**32: 1111 bytes
"""Compatibility helpers to bridge the differences between Python 2 and Python 3.

Similar in purpose to [`six`](https://warehouse.python.org/project/six/). Not generally intended to be used by
third-party software, these are subject to change at any time. Only symbols exported via `__all__` are safe to use.
"""
import sys
__all__ = [
 'py3', 'pypy', 'unicode', 'str']
py3 = sys.version_info > (3, )
pypy = hasattr(sys, 'pypy_version_info')
if py3:
    unicode = str
    str = bytes
    items = dict.items
else:
    unicode = unicode
    str = str
    items = dict.iteritems
try:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

except ImportError:
    from io import StringIO

try:
    from pathlib import PurePosixPath as Path
except ImportError:
    from pathlib2 import PurePosixPath as Path