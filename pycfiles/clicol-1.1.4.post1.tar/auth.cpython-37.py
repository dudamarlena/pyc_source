# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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