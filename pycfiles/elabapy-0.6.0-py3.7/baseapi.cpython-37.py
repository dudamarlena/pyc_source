# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elabapy/baseapi.py
# Compiled at: 2020-05-07 20:22:03
# Size of source mod 2**32: 2383 bytes
import json, logging, os
from typing import Dict, Tuple
from urllib.parse import urljoin
import requests

class Error(Exception):
    __doc__ = 'Base exception class for this module'


class SetupError(Error):
    pass


class BaseAPI(object):
    __doc__ = '\n        Basic api class for elabapy\n    '
    token = ''
    token: str
    endpoint = ''
    endpoint: str
    verify = True
    verify: bool

    def __init__(self, *args, **kwargs):
        self._log = logging.getLogger(__name__)
        self.verify = True
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        if not self.token:
            raise SetupError('No token provided.')
        if not self.endpoint:
            raise SetupError('No endpoint provided.')

    def send_req(self, url: str, params: Dict={}, verb: str='GET', binary: bool=False, param_name: str='data'):
        """ Send the request to the api endpoint. """
        if self.verify == False:
            requests.packages.urllib3.disable_warnings()
        url = urljoin(self.endpoint, url)
        method_map = {'GET':(
          requests.get, {}), 
         'POST':(
          requests.post, {}), 
         'DELETE':(
          requests.delete, {})}
        requests_method, headers = method_map[verb]
        headers.update({'Authorization': self.token})
        kwargs = {'headers': headers, param_name: params, 'verify': self.verify}
        headers_str = str(headers).replace(self.token.strip(), 'TOKEN')
        self._log.debug(f"{verb} {url} {params} {headers_str}")
        req = requests_method(url, **kwargs)
        if not req.ok:
            req.raise_for_status()
        if req.status_code == 204:
            return True
        if binary:
            return req.content
        return req.json()