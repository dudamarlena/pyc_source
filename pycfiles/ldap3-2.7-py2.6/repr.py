# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\repr.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from binascii import hexlify
from .. import STRING_TYPES
try:
    from sys import stdout
    repr_encoding = stdout.encoding
    if not repr_encoding:
        repr_encoding = 'ascii'
except Exception:
    repr_encoding = 'ascii'

def to_stdout_encoding(value):
    if not isinstance(value, STRING_TYPES):
        value = str(value)
    if str is bytes:
        try:
            return value.encode(repr_encoding, 'backslashreplace')
        except UnicodeDecodeError:
            return hexlify(value)

    else:
        try:
            return value.encode(repr_encoding, errors='backslashreplace').decode(repr_encoding, errors='backslashreplace')
        except UnicodeDecodeError:
            return hexlify(value)