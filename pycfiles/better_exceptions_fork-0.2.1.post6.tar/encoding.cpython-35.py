# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/adrie/Desktop/Programmation/better-exceptions/better_exceptions/encoding.py
# Compiled at: 2018-01-15 09:28:31
# Size of source mod 2**32: 725 bytes
from __future__ import absolute_import
import codecs, locale, sys
from .context import PY3
ENCODING = locale.getpreferredencoding()

def to_byte(val):
    unicode_type = str if PY3 else unicode
    if isinstance(val, unicode_type):
        try:
            return val.encode(ENCODING)
        except UnicodeEncodeError:
            if PY3:
                return codecs.escape_decode(val)[0]
            else:
                return val.encode('unicode-escape').decode('string-escape')

    return val


def to_unicode(val):
    if isinstance(val, bytes):
        try:
            return val.decode(ENCODING)
        except UnicodeDecodeError:
            return val.decode('unicode-escape')

        return val