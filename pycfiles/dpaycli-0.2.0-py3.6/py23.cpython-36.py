# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycligraphenebase/py23.py
# Compiled at: 2018-10-14 09:33:48
# Size of source mod 2**32: 942 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes, int, str, chr
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    bytes_types = (
     bytes,)
    string_types = (str,)
    integer_types = (int,)
    text_type = str
    binary_type = bytes
else:
    bytes_types = (
     bytes,)
    string_types = (basestring,)
    integer_types = (int, long)
    text_type = unicode
    binary_type = str

def py23_bytes(item=None, encoding=None):
    if item is None:
        return b''
    else:
        if hasattr(item, '__bytes__'):
            return item.__bytes__()
        if encoding:
            return bytes(item, encoding)
        return bytes(item)


def py23_chr(item):
    if PY2:
        return chr(item)
    else:
        return bytes([item])