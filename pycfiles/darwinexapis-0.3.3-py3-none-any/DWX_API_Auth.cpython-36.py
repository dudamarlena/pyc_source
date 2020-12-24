# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zmlaptop/Desktop/darwinexapis/darwinexapis/API/DWX_API_Auth.py
# Compiled at: 2020-05-09 05:36:27
# Size of source mod 2**32: 4505 bytes
import os, pprint, json, base64, requests, time, pandas as pd

class DWX_API_AUTHENTICATION(object):
    __doc__ = "This class will handle the neccesary work for refreshing the access\n    token. The post response back will be like (access token and refresh token will change):\n    \n    {'access_token': '63ca7671-cf30-3e4d-a13e-0ae789183d73',\n     'expires_in': 3600,\n     'id_token': '...eyJ4NXQi...',\n     'refresh_token': '827c785e-f5ed-33bc-87e5-fb9854fe1f80',\n     'scope': 'openid',\n     'token_type': 'Bearer'}"

    def __init__(self, _auth_creds):
        """_auth_creds is a dictionary with all the credentials:

        Ex:

        {'access_token': '63ca7671-cf30-3e4d-a13e-0ae789183d73',
         'consumer_key': '827c785e-f5ed-33bc-87e5-fb9854',
         'consumer_secret': '827c785e-f5ed-33bc-87e5-fb9854',
         'refresh_token': '827c785e-f5ed-33bc-87e5-fb9854fe1f80'}"""
        self._auth_creds = _auth_creds
        self.expires_in = time.time() + 60
        print(f"[INIT] - Access token will be created again at {self.expires_in} UNIX timestamp")

    def _get_access_refresh_tokens_wrapper(self):
        try:
            self.access_token, self.expires_in, self.refresh_token = self._get_access_refresh_tokens_(self._auth_creds['consumer_key'], self._auth_creds['consumer_secret'], self._auth_creds['refresh_token'])
            if self.access_token is None:
                raise Exception('[INIT] - Request for access token failed > No access_token returned in the response')
            print('[INIT] - Will sleep for some secs...')
            time.sleep(3)
        except Exception as ex:
            print(ex)
        else:
            print('[REFRESH_ELSE] - Will RESET the expires_in variable...')
            self.expires_in = time.time() + (self.expires_in - 300)
            print('[REFRESH_ELSE] - Will add the new access_token and refresh_token to the dictionary')
            self._auth_creds['access_token'] = self.access_token
            self._auth_creds['refresh_token'] = self.refresh_token

    def _get_access_refresh_tokens_(self, client_id, client_secret, refresh_token, token_url='https://api.darwinex.com/token'):
        header_data = {'client_id':client_id, 
         'client_secret':client_secret}
        data = {'grant_type':'refresh_token', 
         'refresh_token':refresh_token}
        headers = {'Authorization': 'Basic {}'.format(base64.b64encode(bytes('{}:{}'.format(header_data['client_id'], header_data['client_secret']).encode('utf-8'))).decode('utf-8'))}
        try:
            _response = requests.post(token_url, headers=headers, data=data, verify=True, allow_redirects=False)
            _response.raise_for_status()
            print('[GET_TOKENS] - Access & Refresh Tokens Retrieved Successfully')
            response_json = json.loads(_response.text)
            return (
             response_json['access_token'], response_json['expires_in'], response_json['refresh_token'])
        except Exception as ex:
            print('[GET_TOKENS] - Access & Refresh Tokens ***NOT*** Retrieved Successfully')
            print('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            return (None, None, None)