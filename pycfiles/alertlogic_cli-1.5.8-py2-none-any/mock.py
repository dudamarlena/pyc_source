# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/abenkevich/defender/alertlogic-cli/alertlogic/tests/mock.py
# Compiled at: 2019-02-11 09:41:07
import httpretty, alertlogic.datacenters, alertlogic.auth, pytest, json

def mock_auth():
    token = {'authentication': {'token': 'TOKEN', 
                          'account': {'id': 'ACCOUNT_ID'}}}
    httpretty.register_uri(httpretty.POST, 'http://test/aims/v1/authenticate', status=200, content_type='text/json', body=json.dumps(token))
    region = alertlogic.datacenters.Datacenters.get_dc('http://test')
    session = alertlogic.auth.Session(region, 'Username', 'Password')
    return session