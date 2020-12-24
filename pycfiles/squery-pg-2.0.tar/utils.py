# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manish/projects/outernet/squery-pg/squery_pg/utils.py
# Compiled at: 2016-03-18 06:21:13
import sys
PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3
if PY3:
    basestring = str
    unicode = str
if PY2:
    unicode = unicode
    basestring = basestring