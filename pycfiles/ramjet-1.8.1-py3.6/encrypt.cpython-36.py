# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/utils/encrypt.py
# Compiled at: 2017-11-06 22:07:48
# Size of source mod 2**32: 495 bytes
import jwt, bcrypt
from ramjet.settings import SECRET_KEY

def generate_passwd(passwd):
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def validate_passwd(passwd, hashed):
    return bcrypt.hashpw(passwd, hashed) == hashed


def generate_token(json_, secret=SECRET_KEY):
    return jwt.encode(json_, secret, algorithm='HS512').decode()


def validate_token(token, secret=SECRET_KEY):
    return jwt.decode(token, secret, verify=True)