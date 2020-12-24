# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/security.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 711 bytes
"""
Module that contains different functions related with security
"""
from __future__ import print_function, division, absolute_import
import base64

def encodeBase64(key, clear):
    enc = list()
    for i in range(len(clear)):
        key_c = key[(i % len(key))]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)

    return base64.urlsafe_b64encode(''.join(enc))


def decodeBase64(key, enc):
    dec = list()
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[(i % len(key))]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)

    return ''.join(dec)