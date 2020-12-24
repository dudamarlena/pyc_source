# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hajime/code/squery-lite/squery_lite/utils.py
# Compiled at: 2016-08-17 06:15:03
# Size of source mod 2**32: 188 bytes
import sys
PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3
if PY3:
    basestring = str
    unicode = str
if PY2:
    unicode = unicode
    basestring = basestring