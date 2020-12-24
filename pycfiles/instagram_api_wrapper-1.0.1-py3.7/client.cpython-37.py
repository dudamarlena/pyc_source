# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/instagram_api_wrapper/client.py
# Compiled at: 2018-08-28 09:41:12
# Size of source mod 2**32: 1251 bytes
import json, requests
from instagram_api_wrapper.exceptions import InstagramApiError

class InstagramApi:
    host = 'https://api.instagram.com/v1'

    class ApiEndpoints(object):
        user_info = '/users/self'
        user_media = '/users/self/media/recent'

    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_user_info(self):
        return self._send_request(url=(self.ApiEndpoints.user_info), params=(self._prepare_data()))

    def get_user_media(self, data=None):
        return self._send_request(url=(self.ApiEndpoints.user_media), params=(self._prepare_data(data)))

    def _send_request(self, url, params=None):
        params = params or {}
        request_url = self._prepare_url(url=url)
        response = requests.get(request_url, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        raise InstagramApiError('Request error. Status code {}'.format(response.status_code))

    def _prepare_url(self, url):
        return '{}/{}'.format(self.host.rstrip('/'), url.lstrip('/'))

    def _prepare_data(self, data=None):
        data = data or {}
        data['access_token'] = self.access_token
        return data