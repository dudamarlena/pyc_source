# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Ofek\Desktop\code\privy\build\lib\privy\utils.py
# Compiled at: 2017-02-14 22:21:45
# Size of source mod 2**32: 405 bytes
from base64 import urlsafe_b64decode, urlsafe_b64encode

def base64_to_bytes(s):
    return urlsafe_b64decode(s)


def bytes_to_base64(s):
    return urlsafe_b64encode(s).decode('ascii')


def ensure_bytes(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    return s


def ensure_unicode(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return s