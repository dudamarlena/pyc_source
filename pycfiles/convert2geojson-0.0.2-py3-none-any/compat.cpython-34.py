# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/compat.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1157 bytes
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