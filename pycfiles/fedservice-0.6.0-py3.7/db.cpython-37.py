# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/metadata_api/db.py
# Compiled at: 2019-09-25 06:09:07
# Size of source mod 2**32: 1237 bytes
import base64, json, logging
from urllib.parse import quote_plus
import requests
from cryptojwt.jwt import JWT
logger = logging.getLogger(__name__)

def db_make_entity_statement(db_url, authn_info, key_jar, lifetime, sign_alg='ES256', **kwargs):
    iss = kwargs['iss']
    try:
        sub = kwargs['sub']
    except KeyError:
        sub = iss

    credentials = '{}:{}'.format(authn_info['user'], authn_info['password'])
    authz = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    http_args = {'headers': {'Authorization': 'Basic {}'.format(authz)}}
    if db_url.endswith('/'):
        _url = '{}{}'.format(db_url, quote_plus(sub))
    else:
        _url = '{}/{}'.format(db_url, quote_plus(sub))
    resp = (requests.request)('GET', _url, **http_args)
    if resp.status_code == 200:
        payload = json.loads(resp.text)
        packer = JWT(key_jar=key_jar, iss=iss, lifetime=lifetime, sign=True,
          sign_alg=sign_alg)
        return packer.pack(payload)
    raise SystemError('DB not accessible "{}"'.format(resp.text))