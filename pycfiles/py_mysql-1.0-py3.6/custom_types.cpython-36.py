# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\custom_types.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 1665 bytes
"""Custom Python types used by MySQL Connector/Python"""
import sys

class HexLiteral(str):
    __doc__ = 'Class holding MySQL hex literals'

    def __new__(cls, str_, charset='utf8'):
        if sys.version_info[0] == 2:
            hexed = ['%02x' % ord(i) for i in str_.encode(charset)]
        else:
            hexed = ['%02x' % i for i in str_.encode(charset)]
        obj = str.__new__(cls, ''.join(hexed))
        obj.charset = charset
        obj.original = str_
        return obj

    def __str__(self):
        return '0x' + self