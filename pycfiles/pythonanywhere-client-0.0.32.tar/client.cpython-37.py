# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\hakancelik96\pythonanywhere-python-client\pythonanywhere_client\client.py
# Compiled at: 2019-07-04 16:10:48
# Size of source mod 2**32: 1668 bytes
import requests, re, inspect

class Client:
    base_uri = 'https://www.pythonanywhere.com'

    def __init__(self, username, token):
        self.username = username
        self.headers = dict(Authorization=f"Token {token}")

    def _create_api_uri(self, op, name, path, api_version='v0'):
        return f"{self.base_uri}/api/{api_version}/user/{self.username}/{op}/{name}/{path}"

    def _requests(self, method, op, name, path, data):
        uri = self._create_api_uri(op, name, path)
        return getattr(requests, method)(uri,
          timeout=10,
          headers=(self.headers),
          data=data)


def get_variable(obj, text):
    regex = '{self\\.(.*)}'
    matches = re.finditer(regex, text, re.DOTALL)
    for match in matches:
        match_text = text[match.span()[0]:match.span()[1]]
        remove_match_text = text.replace(match_text, '')
        variable = str(getattr(obj, match.group(1)))
        return remove_match_text + variable

    return text


def client_decorator(op, name='', path='', method=None):

    def client_f(func):

        def wraps(*args, **kwargs):
            get_parameters = (inspect.getcallargs)(func, *args, **kwargs)
            obj = get_parameters['self']
            del get_parameters['self']
            return getattr(obj.client, '_requests')(method=(method or func.__name__),
              op=op,
              name=(get_variable(obj, name)),
              path=path,
              data=(get_parameters or dict()))

        return wraps

    return client_f