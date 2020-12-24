# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/requestbin/service.py
# Compiled at: 2015-02-18 16:03:16
"""
The service module
"""
import json, requests
from requests.structures import CaseInsensitiveDict as cidict
from requests.adapters import HTTPAdapter
from tools import pathjoin
DEFAULT_SERVICE_URL = 'http://requestb.in/'

class Service(object):
    """the requestb.in handle object"""

    def __init__(self, url=DEFAULT_SERVICE_URL, auth=None, adapter=HTTPAdapter(max_retries=10)):
        self.url = url
        self.session = requests.Session()
        self.session.mount(url, adapter)
        self.auth = auth
        self.adapter = adapter

    def send(self, request):
        """send a request to self.url authenticated with self.auth"""
        return self.session.send(request(self.url, self.auth))


class ServiceRequest(object):
    """Service-compatible request object"""

    def __init__(self, method, path='/', data={}, headers=cidict({'content-type': 'application/json', 'accept': 'application/json'})):
        self.method = method
        self.path = path
        if 'content-type' in headers and headers['content-type'] == 'application/json':
            self.data = json.dumps(data)
        self.headers = headers

    def __call__(self, url, auth=None):
        """return a prepared request to be sent"""
        return requests.Request(self.method, pathjoin(self.path, url=url), auth=auth, headers=self.headers, data=self.data).prepare()