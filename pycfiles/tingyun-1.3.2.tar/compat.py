# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/requests/packages/chardet/compat.py
# Compiled at: 2016-06-30 06:13:10
import sys
if sys.version_info < (3, 0):
    base_str = (
     str, unicode)
else:
    base_str = (
     bytes, str)

def wrap_ord(a):
    if sys.version_info < (3, 0) and isinstance(a, base_str):
        return ord(a)
    else:
        return a