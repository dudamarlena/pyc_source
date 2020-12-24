# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/client/requester.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 5399 bytes
from future import standard_library
from requests.adapters import HTTPAdapter
standard_library.install_aliases()
from builtins import str
from builtins import object
import requests
from urllib.parse import urlparse
from pprint import pprint
import json, sys
from requests.exceptions import HTTPError
from chisubmit.client.exceptions import UnknownObjectException, ChisubmitRequestException, BadRequestException, UnauthorizedException
import base64, datetime

def json_serial(obj):
    if isinstance(obj, datetime.timedelta):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError('Type not serializable')


class Requester(object):

    def __init__(self, login_or_token, password, base_url, ssl_verify=True):
        self._Requester__base_url = base_url
        self._Requester__headers = {}
        self._Requester__headers['content-type'] = 'application/json'
        if login_or_token is not None and password is not None:
            basic_str = '{}:{}'.format(login_or_token, password)
            basic_str = bytes(basic_str, encoding='utf8')
            self._Requester__headers['Authorization'] = b'Basic ' + base64.b64encode(basic_str)
        elif login_or_token is not None:
            self._Requester__headers['Authorization'] = 'Token %s' % login_or_token
        self._Requester__ssl_verify = ssl_verify
        self._Requester__session = requests.Session()
        self._Requester__session.mount(base_url, HTTPAdapter(max_retries=5))

    def request(self, method, resource, data=None, headers=None, params=None):
        if resource.startswith('/'):
            url = self._Requester__base_url + resource
        else:
            url = resource
        all_headers = {}
        all_headers.update(self._Requester__headers)
        if headers is not None:
            all_headers.update(headers)
        if data is not None:
            data = json.dumps(data, default=json_serial)
        retry = 20
        while retry >= 0:
            try:
                response = self._Requester__session.request(url=url, method=method, params=params, data=data, headers=all_headers, verify=self._Requester__ssl_verify)
                if response.status_code == 400:
                    raise BadRequestException(method, url, params, data, all_headers, response)
                else:
                    if 400 < response.status_code < 500:
                        if response.status_code == 401:
                            raise UnauthorizedException(method, url, params, data, all_headers, response)
                        if response.status_code == 404:
                            raise UnknownObjectException(method, url, params, data, all_headers, response)
                        else:
                            raise ChisubmitRequestException(method, url, params, data, all_headers, response)
                    elif 500 <= response.status_code < 600:
                        raise ChisubmitRequestException(method, url, params, data, all_headers, response)
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = {'data': response.text}

                return (
                 response.headers, response_data)
            except requests.exceptions.ConnectionError:
                retry -= 1
                if retry < 0:
                    raise