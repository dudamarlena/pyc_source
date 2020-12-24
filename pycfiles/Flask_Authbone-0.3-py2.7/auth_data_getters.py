# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/authbone/auth_data_getters.py
# Compiled at: 2016-06-21 08:46:25
from flask import request
from .authentication import AuthDataDecodingException

def form_data_getter():
    auth_data = dict()
    try:
        auth_data['username'] = request.form['username']
    except KeyError:
        raise AuthDataDecodingException('bad credentials: missing "username"')

    try:
        auth_data['password'] = request.form['password']
    except KeyError:
        raise AuthDataDecodingException('bad credentials: missing "password"')

    return auth_data


def basic_auth_getter():
    return request.authorization