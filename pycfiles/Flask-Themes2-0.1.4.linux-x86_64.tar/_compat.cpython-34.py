# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/flask_themes2/_compat.py
# Compiled at: 2014-02-06 15:42:26
# Size of source mod 2**32: 587 bytes
"""
    Look here for more information:
    https://github.com/mitsuhiko/flask/blob/master/flask/_compat.py
"""
import sys
PY2 = sys.version_info[0] == 2
if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()