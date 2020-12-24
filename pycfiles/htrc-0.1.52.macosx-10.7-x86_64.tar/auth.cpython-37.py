# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/auth.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 1718 bytes
from base64 import b64encode
from getpass import getpass
import http.client, ssl, time, requests, requests.auth, htrc.config

def get_jwt_token():
    username, password = credential_prompt()
    client_id, client_secret = htrc.config.get_credentials()
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type':'password',  'username':username, 
     'password':password, 
     'scope':'openid'}
    url = htrc.config.get_idp_url()
    r = requests.post(url, data=data, auth=auth)
    data = r.json()
    if 'error' not in data:
        expiration = int(time.time()) + data['expires_in']
        return (data['id_token'], expiration)
    if data['error'] == 'invalid_grant':
        print('Invalid username or password. Please try again.\n')
        return get_jwt_token()
    raise RuntimeError('JWT token retrieval failed: {}'.format(data['error']))


def credential_prompt():
    """
    A prompt for entering HathiTrust Research Center credentials.
    """
    print('Please enter your HathiTrust Research Center credentials.')
    username = input('HTRC Username: ')
    password = getpass('HTRC Password: ')
    if not (username and password):
        print('Invalid username or password. Please try again.\n')
        return credential_prompt()
    return (username, password)


if __name__ == '__main__':
    token, expiration = get_jwt_token()
    htrc.config.save_jwt_token(token, expiration)