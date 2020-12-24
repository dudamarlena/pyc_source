# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewels/GitHub/MegaQC/megaqc/compat.py
# Compiled at: 2018-07-06 11:43:41
"""Python 2/3 compatibility module."""
from builtins import bytes
import sys
PY2 = int(sys.version[0]) == 2
if PY2:
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
else:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)