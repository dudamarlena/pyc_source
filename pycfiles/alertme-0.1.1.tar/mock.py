# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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