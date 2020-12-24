# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/mediators/token_exchange/util.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from datetime import datetime, timedelta
TOKEN_LIFE_IN_HOURS = 8
AUTHORIZATION = 'authorization_code'
REFRESH = 'refresh_token'

class GrantTypes(object):
    AUTHORIZATION = AUTHORIZATION
    REFRESH = REFRESH


def token_expiration():
    return datetime.utcnow() + timedelta(hours=TOKEN_LIFE_IN_HOURS)