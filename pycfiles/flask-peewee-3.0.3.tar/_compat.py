# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../flask_peewee/_compat.py
# Compiled at: 2018-01-17 11:50:43
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr
    reduce = reduce
else:
    text_type = str
    string_types = (str,)
    unichr = chr
    from functools import reduce