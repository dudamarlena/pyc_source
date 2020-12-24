# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slink/core/providers/bitly.py
# Compiled at: 2020-04-12 10:26:14
# Size of source mod 2**32: 1059 bytes
import requests, cerberus
from core.errors import WrongResponse, Forbidden
from core.utils import reraise_requests
from ..main import Provider

class BitlyProvider(Provider):
    _SHORTEN_API_URL = 'https://api-ssl.bitly.com/v4/shorten'
    _RESPONSE_SCHEMA = {'link': {'type': 'string'}}

    def __init__(self, access_token: str):
        self._access_token = access_token

    @reraise_requests
    def shorten_url(self, url: str) -> str:
        data = {'long_url': url}
        headers = {'Authorization':f"Bearer {self._access_token}", 
         'Accept':'application/json'}
        resp = requests.post((self._SHORTEN_API_URL), headers=headers, json=data, timeout=5)
        if resp.status_code == 403:
            raise Forbidden
        json_resp = resp.json()
        is_valid = cerberus.Validator((self._RESPONSE_SCHEMA), allow_unknown=True).validate(json_resp)
        if not is_valid:
            raise WrongResponse
        return json_resp['link']