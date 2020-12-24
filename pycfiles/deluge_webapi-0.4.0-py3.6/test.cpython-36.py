# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webapi/test.py
# Compiled at: 2019-02-21 09:08:47
# Size of source mod 2**32: 1116 bytes
import requests
from os import environ
PASSWORD = environ.get('WEBAPI_PASSWORD', '*****')
COOKIES = None
REQUEST_ID = 0

def send_request(method, params=None):
    global COOKIES
    global REQUEST_ID
    REQUEST_ID += 1
    try:
        response = requests.post('http://localhost:8112/json',
          json={'id':REQUEST_ID, 
         'method':method,  'params':params or []},
          cookies=COOKIES)
    except requests.exceptions.ConnectionError:
        raise Exception('WebUI seems to be unavailable. Run deluge-web or enable WebUI plugin using other thin client.')

    data = response.json()
    error = data.get('error')
    if error:
        msg = error['message']
        if msg == 'Unknown method':
            msg += '. Check WebAPI is enabled.'
        raise Exception('API response: %s' % msg)
    COOKIES = response.cookies
    return data['result']


if not send_request('auth.login', [PASSWORD]):
    raise AssertionError('Unable to log in. Check password.')
else:
    version_number = send_request('webapi.get_api_version')
    assert version_number
print('WebAPI version: %s' % version_number)
print('Success')