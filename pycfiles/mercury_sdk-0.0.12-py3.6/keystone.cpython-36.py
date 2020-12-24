# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/auth/keystone.py
# Compiled at: 2018-11-06 13:31:04
# Size of source mod 2**32: 1855 bytes
import getpass, os, requests
KEYSTONE_USER_ENV = 'KEYSTONE_USER'
KEYSTONE_API_URL_ENV = 'KEYSTONE_API_URL'

def add_arguments(login_parser):
    login_parser.add_argument('--keystone-api-url', default=(os.environ.get(KEYSTONE_API_URL_ENV)),
      help='[keystone plugin] keystone url to use')
    login_parser.add_argument('--keystone-user', default=(os.environ.get(KEYSTONE_USER_ENV)),
      help='[keystone plugin] keystone user to use')


def authenticate(configuration):
    auth_config = configuration['auth']
    _payload = {'auth': {}}
    if auth_config['type'] == 'password':
        _payload['auth']['passwordCredentials'] = {'username':os.environ.get(KEYSTONE_USER_ENV) or auth_config['username'], 
         'password':auth_config.get('password') or getpass.getpass()}
    else:
        if auth_config['type'] == 'rax-rsa':
            _payload['auth']['RAX-AUTH:rsaCredentials'] = {'username':auth_config['username'],  'tokenKey':getpass.getpass('PIN + RSA: ')}
        else:
            raise Exception('Auth type is not supported')
    if 'domain' in auth_config:
        _payload['auth'][auth_config['domain']['key']] = {'name': auth_config['domain']['name']}
    response = requests.post((os.environ.get(KEYSTONE_API_URL_ENV) or auth_config['url']),
      json=_payload)
    if not response.ok:
        raise Exception('Error authenticating : {}'.format(response.status_code))
    response = response.json()
    return {'token':response['access']['token']['id'], 
     'expires_at':response['access']['token']['expires']}


def invalidate(configuration, token_data):
    pass