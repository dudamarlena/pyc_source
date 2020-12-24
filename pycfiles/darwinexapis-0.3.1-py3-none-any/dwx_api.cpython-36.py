# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eriz/Desktop/darwinexapis/darwinexapis/API/dwx_api.py
# Compiled at: 2020-05-04 07:50:16
# Size of source mod 2**32: 5729 bytes
"""
    DWX_API - Superclass for all sub-APIs
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 29, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os, requests, json, time
from darwinexapis.API.DWX_API_Auth import DWX_API_AUTHENTICATION

class Decorators:

    @staticmethod
    def refreshTokenDecorator_APIs(func_to_be_decorated):
        """Example use > put the decorator upfront the method that will make request:

        @refreshTokenDecorator
        def someRequest(self):
            # make our API request
            pass"""

        def wrapper_of_the_func(self, *args, **kwargs):
            if time.time() > self.AUTHENTICATION.expires_in:
                print('\n[DECORATOR] - The expiration time has REACHED > ¡Generate TOKENS!')
                self.AUTHENTICATION._get_access_refresh_tokens_wrapper()
            else:
                print('\n[DECORATOR] - The expiration time has NOT reached yet > Continue...')
            return func_to_be_decorated(self, *args, **kwargs)

        return wrapper_of_the_func


class DWX_API(object):

    def __init__(self, _auth_creds='', _api_url='https://api.darwinex.com', _api_name='darwininfo', _version=1.5, _demo=False):
        self.AUTHENTICATION = DWX_API_AUTHENTICATION(_auth_creds)
        self._url = '{}/{}/{}'.format(_api_url, _api_name, _version)

    def _construct_auth_post_headers(self):
        self._auth_headers = {'Authorization': f"Bearer {self.AUTHENTICATION._auth_creds['access_token']}"}
        self._post_headers = {**(self._auth_headers), **{'Content-type':'application/json', 
         'Accept':'application/json'}}

    @Decorators.refreshTokenDecorator_APIs
    def _Call_API_(self, _endpoint, _type, _data, _json=True, _stream=False):
        """Call any endpoint provided in the Darwinex API documentation, and get JSON."""
        self._construct_auth_post_headers()
        if _type not in ('GET', 'POST', 'PUT', 'DELETE'):
            print('Bad request type')
            return
        try:
            if _type == 'GET':
                _ret = requests.get((self._url + _endpoint), headers=(self._auth_headers),
                  verify=True)
                print(f"**** FULL URL ENDPOINT ****: {_ret.url}")
            else:
                if _type == 'PUT':
                    _ret = requests.put((self._url + _endpoint), headers=(self._post_headers),
                      data=_data,
                      verify=True)
                    print(f"**** FULL URL ENDPOINT ****: {_ret.url}")
                else:
                    if _type == 'DELETE':
                        _ret = requests.delete((self._url + _endpoint), headers=(self._auth_headers),
                          verify=True)
                        print(f"**** FULL URL ENDPOINT ****: {_ret.url}")
                    else:
                        if len(_data) == 0:
                            print('Data is empty..')
                            return
                        if _stream:
                            self._post_headers['connection'] = 'keep-alive'
                            return requests.Request('POST', (self._url + _endpoint),
                              headers=(self._post_headers),
                              data=_data)
                        _ret = requests.post((self._url + _endpoint), data=_data,
                          headers=(self._post_headers),
                          verify=True)
            if _json:
                return _ret.json()
            else:
                return _ret
        except Exception as ex:
            print('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            print(f"Response request code: {_ret.status_code}")
            print(f"Response request URL: {_ret.url}")
            print(f"Response request Data: {_ret.text}")