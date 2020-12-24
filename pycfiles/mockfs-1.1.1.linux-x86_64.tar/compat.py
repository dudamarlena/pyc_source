# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/src/python/mockfs/env27/lib/python2.7/site-packages/mockfs/compat.py
# Compiled at: 2020-03-21 23:28:53
from __future__ import absolute_import, division, unicode_literals
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    import __builtin__ as builtins
    int_types = (int, long)
    string_types = (str, unicode)
else:
    import builtins
    int_types = (
     int,)
    string_types = (str,)