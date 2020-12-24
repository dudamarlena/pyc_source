# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kclient/client.py
# Compiled at: 2018-03-10 04:47:03
"""
    kclient.client
    ~~~~~~~~~~~~

    Python wrapper for k-client API.
"""
import os, requests, logging, shutil
from .helper import detect_filename
from requests.exceptions import RequestException

class Client(object):
    ROOT_URL = 'https://client-k.hot.sonydna.com'
    requests = None

    def __init__(self, **kwargs):
        options = [
         'username', 'token', 'version', 'user-agent']
        for option in options:
            if option in kwargs:
                setattr(self, option, kwargs[option])
            else:
                setattr(self, option, None)

        if self.requests is None:
            self.requests = requests
        return

    def _headers(self):
        return {'Content-Type': 'application/json', 'Accept': '*/*', 
           'User-Agent': getattr(self, 'user-agent'), 
           'X-API-Version': getattr(self, 'version')}

    def _body(self):
        return {'username': getattr(self, 'username'), 
           'token': getattr(self, 'token')}

    def _post(self, path, params=None):
        """POST request.
        :param path:
        :param params:
        """
        url = self.ROOT_URL + path
        json = params or {}
        json.update(self._body())
        json = dict([ (k, v) for k, v in json.items() if v is not None ])
        try:
            r = self.requests.post(url=url, json=json, headers=self._headers())
            json = r.json()
            if r.status_code == 200 and json['status'] == 'OK':
                return json['result']
            logging.warning('api error. %s' % json)
            return
        except RequestException as e:
            logging.error(e)
            return

        return

    def download(self, url, out=None):
        """

        :param url:
        :param out:
        :return:
        """
        if out is None:
            out = detect_filename(url)
        if os.path.exists(path=out):
            return
        else:
            res = self.requests.get(url, stream=True, headers=self._headers())
            with open(out, 'wb') as (fp):
                logging.debug('Downlonad:' + out)
                shutil.copyfileobj(res.raw, fp)
            return

    def unread(self):
        return self._post('/sysinfo/unread')