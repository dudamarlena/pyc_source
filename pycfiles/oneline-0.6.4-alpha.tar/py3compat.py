# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/py3compat.py
# Compiled at: 2014-07-29 17:29:28
"""Utility functions and definitions for python3 compatibility."""
import sys
PY3 = sys.version_info[0] == 3
if PY3:
    import codecs
    from io import BytesIO as StringIO

    def b(s):
        return codecs.latin_1_encode(s)[0]


    def bytes_from_hex(h):
        return bytes.fromhex(h)


    binary_type = bytes
    text_type = str
    next_item = '__next__'
else:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    def b(s):
        return s


    def bytes_from_hex(h):
        return h.decode('hex')


    binary_type = str
    text_type = unicode
    next_item = 'next'
string_types = (binary_type, text_type)