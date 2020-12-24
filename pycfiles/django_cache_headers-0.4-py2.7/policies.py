# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/tests/policies.py
# Compiled at: 2017-03-22 04:19:49
import datetime
from cache_headers.utils import httpdate

def custom_policy(request, response, user, age):
    if user.username == 'user':
        response['X-Is-Special-User'] = 1
    else:
        response['X-Is-Special-User'] = 0
    response['Vary'] = 'Accept-Encoding,X-Is-Special-User'