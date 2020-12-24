# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/auth/coding.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 258 bytes
import jwt

def encode(payload, secret='', algorithm='HS256'):
    return jwt.encode(payload, secret, algorithm=algorithm).decode('utf-8')


def decode(encoded, secret='', algorithms=['HS256']):
    return jwt.decode(encoded, secret, algorithms=algorithms)