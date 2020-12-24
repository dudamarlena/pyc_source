# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/keystoneredis/common/keys.py
# Compiled at: 2013-02-13 13:57:35
from base64 import b64encode
from base64 import b64decode

def revoked():
    return 'revoked'


def token(token_id):
    return ('token {0}').format(token_id)


def usertoken(user_id, token_id):
    if token_id == '*':
        return ('usertoken {0} *').format(b64encode(user_id))
    else:
        return ('usertoken {0} {1}').format(b64encode(user_id), token_id)


def parse_token(key):
    t, token = key.split(' ', 1)
    if t != 'token':
        raise ValueError('Expected token key: ' + key)
    return token


def parse_usertoken(key):
    t, user_b64, token = key.split(' ', 2)
    if t != 'usertoken':
        raise ValueError('Expected usertoken key: ' + key)
    return (
     b64decode(user_b64), token)