# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\lib\dump.py
# Compiled at: 2013-09-08 09:59:18
from __future__ import division, absolute_import, print_function, unicode_literals
try:
    from .backwardcompat import *
except:
    from backwardcompat import *

def plain_type(obj):
    buf = unicode(type(obj)).replace(b"'", b'').replace(b'type ', b'').replace(b'class ', b'').replace(b'<', b'[').replace(b'>', b']')
    return buf


def plain(obj, level=0):
    if obj is None:
        buf = b'None'
        return buf
    if isinstance(obj, numeric_types):
        buf = unicode(obj)
        return buf
    else:
        if isinstance(obj, bytes):
            try:
                buf = (b"'{0}'").format(u(obj).rstrip(b'\r\n'))
            except:
                buf = (b'repr: {0!r}').format(obj)

            return buf
        if isinstance(obj, string_types):
            try:
                buf = (b"'{0}'").format(unicode(obj).rstrip(b'\r\n'))
            except:
                buf = (b'repr: {0!r}').format(obj)

            return buf
        if isinstance(obj, simple_types):
            buf = (b"'{0}'").format(unicode(obj))
            return buf
        if level > 10:
            return (b'repr: {0!r}').format(obj)
        buf = b''
        wrap = b'    ' * level
        if isinstance(obj, list):
            if obj:
                buf += b'[\n'
                for key in obj:
                    buf += wrap + (b'    {0}\n').format(plain(key, level + 1))

                buf += wrap + b']'
            else:
                buf += b'[]'
            return buf
        if isinstance(obj, collections_types):
            buf += b'('
            for key in obj:
                buf += (b'{0}, ').format(plain(key, level + 1))

            buf += b')'
            return buf
        if isinstance(obj, dict):
            buf += b'{\n'
            for key in sorted(obj.keys(), key=unicode):
                val = obj[key]
                key = plain(key)
                buf += wrap + (b'    {0:16}: {1}\n').format(key, plain(val, level + 1))

            buf += wrap + b'}'
            return buf
        if level > 2:
            return (b'repr: {0!r}').format(obj)
        buf += (b'{0}{{\n').format(plain_type(obj))
        for key in dir(obj):
            try:
                val = getattr(obj, key)
            except Exception as e:
                val = (b'*** {0} ***').format(e)

            if key[0:2] != b'__' and not callable(val):
                buf += wrap + (b'    {0:16}: {1}\n').format(key, plain(val, level + 1))

        buf += wrap + b'}'
        return buf