# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/onedesk/auth/auth.py
# Compiled at: 2019-03-13 18:16:10
# Size of source mod 2**32: 519 bytes
import json, logging
logger = logging.getLogger('main')

def get_token(session, instance, username, password):
    headers = {'Content-Type': 'application/json'}
    token_payload = {'username':username,  'password':password,  'grant_type':'password'}
    response = session.post((instance + '/api/auth-service/token/'), headers=headers, json=token_payload)
    logger.debug('Get token: %s', response.status_code)
    return json.loads(response.text)['access_token']