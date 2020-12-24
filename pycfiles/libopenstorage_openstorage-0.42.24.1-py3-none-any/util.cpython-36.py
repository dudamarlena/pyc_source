# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/wheel/wheel/util.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 924 bytes
import base64, io, sys
if sys.version_info[0] < 3:
    text_type = unicode
    StringIO = io.BytesIO

    def native(s, encoding='utf-8'):
        if isinstance(s, unicode):
            return s.encode(encoding)
        else:
            return s


else:
    text_type = str
    StringIO = io.StringIO

    def native(s, encoding='utf-8'):
        if isinstance(s, bytes):
            return s.decode(encoding)
        else:
            return s


def urlsafe_b64encode(data):
    """urlsafe_b64encode without padding"""
    return base64.urlsafe_b64encode(data).rstrip(b'=')


def urlsafe_b64decode(data):
    """urlsafe_b64decode without padding"""
    pad = b'=' * (4 - (len(data) & 3))
    return base64.urlsafe_b64decode(data + pad)


def as_unicode(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    else:
        return s


def as_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    else:
        return s