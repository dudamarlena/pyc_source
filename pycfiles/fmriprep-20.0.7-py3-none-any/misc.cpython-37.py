# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/distlib/_backport/misc.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 971 bytes
"""Backports for individual classes and functions."""
import os, sys
__all__ = [
 'cache_from_source', 'callable', 'fsencode']
try:
    from imp import cache_from_source
except ImportError:

    def cache_from_source(py_file, debug=True):
        ext = debug and 'c' or 'o'
        return py_file + ext


try:
    callable = callable
except NameError:
    from collections import Callable

    def callable(obj):
        return isinstance(obj, Callable)


try:
    fsencode = os.fsencode
except AttributeError:

    def fsencode(filename):
        if isinstance(filename, bytes):
            return filename
        if isinstance(filename, str):
            return filename.encode(sys.getfilesystemencoding())
        raise TypeError('expect bytes or str, not %s' % type(filename).__name__)