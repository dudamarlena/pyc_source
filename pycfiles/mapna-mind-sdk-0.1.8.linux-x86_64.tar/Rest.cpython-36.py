# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/Rest.py
# Compiled at: 2020-01-16 08:58:49
# Size of source mod 2**32: 2144 bytes
import json, requests
from simplejson.errors import JSONDecodeError
import mapnamindsdk.Constants as Constants
from requests import Session, RequestException

class Rest(Session):

    def __init__(self, base_url=f"{Constants.DATASERVICE_SERVER_IP}:{Constants.DATASERVICE_PORT}", path='/', params=None, header={'Content-Type': 'application/json; charset=utf-8'}, response_encoding='utf-8'):
        super().__init__()
        self.base_url = base_url
        self.path = path
        self.params = params
        self.header = header
        self.response_encoding = response_encoding

    def _do_it(self, verb: str='get', get_json: bool=True):
        try:
            full_url = f"{self.base_url}{self.path}"
            response = requests.request(method=verb,
              url=full_url,
              headers=(self.header),
              data=(json.dumps(self.params)))
            if get_json:
                if response:
                    return response.json()
            return response.text
        except JSONDecodeError as jerr:
            print('JSON Decode Error:', str(jerr))
        except RequestException as rerr:
            print(f"Request Exception:\n Message:{str(rerr)}")

    def get(self, get_json: bool=True):
        return self._do_it('get', get_json)

    def post(self, get_json: bool=True):
        return self._do_it('post', get_json)

    def put(self, get_json: bool=True):
        return self._do_it('put', get_json)

    def delete(self, get_json: bool=True):
        return self._do_it('delete', get_json)

    def head(self, get_json: bool=True):
        return self._do_it('head', get_json)


if __name__ == '__main__':
    params = {'par1':'value1',  'par2':'take it easy'}
    post_req = Rest(base_url='http://localhost:7175', path='/test',
      params=params)
    print(post_req.post())