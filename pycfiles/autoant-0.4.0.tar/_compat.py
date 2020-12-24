# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: autoant/_compat.py
# Compiled at: 2014-09-25 09:51:45
"""
    Some py2/py3 compatibility support based on a stripped down
    version of six so we don't have to depend on a specific version
    of it.

    :copyright: (c) 2013 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
PY2 = sys.version_info[0] == 2
VER = sys.version_info
if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    def as_unicode(s):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return str(s)


else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    def as_unicode(s):
        if isinstance(s, str):
            return s.decode('utf-8')
        return unicode(s)