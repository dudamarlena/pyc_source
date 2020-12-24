# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/auth/coding.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 258 bytes
import jwt

def encode(payload, secret='', algorithm='HS256'):
    return jwt.encode(payload, secret, algorithm=algorithm).decode('utf-8')


def decode(encoded, secret='', algorithms=['HS256']):
    return jwt.decode(encoded, secret, algorithms=algorithms)