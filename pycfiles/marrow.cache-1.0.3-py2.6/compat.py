# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/marrow/cache/compat.py
# Compiled at: 2014-12-11 02:18:40
"""Compatibility helpers to bridge the differences between Python 2 and Python 3.

Similar in purpose to [`six`](https://warehouse.python.org/project/six/).
"""
import sys
py2 = sys.version_info < (3, )
py3 = sys.version_info > (3, )
pypy = hasattr(sys, 'pypy_version_info')
if py3:
    native = str
    unicode = str
    str = bytes
    iterkeys = dict.keys
    itervalues = dict.values
    iteritems = dict.items
else:
    native = str
    unicode = unicode
    str = str
    range = xrange
    iterkeys = dict.iterkeys
    itervalues = dict.itervalues
    iteritems = dict.iteritems