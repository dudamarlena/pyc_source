# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/loc-project/loc/compat.py
# Compiled at: 2018-10-10 14:29:40
"""
For PY2/3 compatible.
"""
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:

    def iterkeys(d, **kw):
        return iter(d.keys(**kw))


    def itervalues(d, **kw):
        return iter(d.values(**kw))


    def iteritems(d, **kw):
        return iter(d.items(**kw))


    def iterlists(d, **kw):
        return iter(d.lists(**kw))


else:

    def iterkeys(d, **kw):
        return d.iterkeys(**kw)


    def itervalues(d, **kw):
        return d.itervalues(**kw)


    def iteritems(d, **kw):
        return d.iteritems(**kw)


    def iterlists(d, **kw):
        return d.iterlists(**kw)