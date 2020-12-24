# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nekos\http.py
# Compiled at: 2018-05-15 13:33:22
# Size of source mod 2**32: 1066 bytes
import requests

class RequestsApi:

    def __init__(self, base_url, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self._RequestsApi__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def get(self, url, **kwargs):
        return (self.session.get)((self.base_url + url), **kwargs)

    def post(self, url, **kwargs):
        return (self.session.post)((self.base_url + url), **kwargs)

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsApi._RequestsApi__deep_merge(value, node)
            else:
                destination[key] = value

        return destination


baseurl = RequestsApi('https://nekos.life/api/v2')

def get(endpoint):
    r = baseurl.get(endpoint)
    return r.json()