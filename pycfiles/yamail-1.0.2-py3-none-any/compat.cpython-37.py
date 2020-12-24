# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/compat.py
# Compiled at: 2018-06-18 12:54:37
# Size of source mod 2**32: 99 bytes
import os, sys
PY3 = sys.version_info[0] == 3
text_type = (str,) if PY3 else (str, unicode)