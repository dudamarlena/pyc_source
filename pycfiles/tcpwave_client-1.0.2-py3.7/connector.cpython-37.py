# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tcpwave_client/connector.py
# Compiled at: 2020-04-14 09:34:11
# Size of source mod 2**32: 4400 bytes
import requests, json
from requests.auth import HTTPBasicAuth
from requests import Session
from tcpwave_client import APICallFailedException, UnsupportedMethodException

class Connector(object):
    __doc__ = "\n        Class to handle connection to Tcpwave's IPAM\n    "

    def __init__(self, cert=None, key=None, user=None, password=None, verify=False):
        """
        creates connector object either with client certificates or with client credentials
        :param cert:
        :param key:
        :param user:
        :param password:
        :param verify:
        """
        self.session = Session()
        if cert is not None or key is not None:
            self.session.cert = (
             cert, key)
        else:
            if user is not None and password is not None:
                self.session.auth = HTTPBasicAuth(user, password)
            else:
                raise Exception('Missing certificates or user credentials')
        adapter = requests.adapters.HTTPAdapter(pool_connections=10,
          pool_maxsize=10,
          max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.verify = verify
        self.url = 'https://%s:7443/tims/rest%s'

    def __construct_url(self, server, rel_url):
        self.url = str(self.url) % (server, rel_url)

    def get_object(self, payload):
        """
        Make GET call
        :param payload:
        :return:
        """
        if '%s' in self.url:
            self._Connector__construct_url(payload['provider']['host'], payload['rel_url'])
        else:
            rsp = self.session.get(url=(self.url), headers=(payload.get('headers')), params=(payload.get('params')))
            status_code = rsp.status_code
            if status_code == 200:
                if len(rsp.content):
                    try:
                        data = rsp.json()
                    except Exception:
                        data = rsp.content

                    return data
            else:
                raise APICallFailedException('API call failed. Msg :: ' + str(rsp.content.decode('utf-8')))

    def create_object(self, payload):
        """
        Make PUT/POST call to create/update object
        :param payload:
        :return:
        """
        method = payload['method']
        if method not in ('PUT', 'POST'):
            raise UnsupportedMethodException('method %s not supported' % method)
        if '%s' in self.url:
            self._Connector__construct_url(payload['provider']['host'], payload['rel_url'])
        else:
            if method == 'POST':
                rsp = self.session.post(url=(self.url), headers=(payload.get('headers')), params=(payload.get('params')), data=(json.dumps(payload.get('body'))))
            else:
                rsp = self.session.put(url=(self.url), headers=(payload.get('headers')), params=(payload.get('params')), data=(json.dumps(payload.get('body'))))
            status_code = rsp.status_code
            if status_code == 200 or status_code == 201:
                if len(rsp.content):
                    return rsp.json()
                    return '{"msg": "Successful"}'
                else:
                    pass
            raise APICallFailedException('API call failed. Msg :: ' + str(rsp.content.decode('utf-8')))

    def delete_object(self, payload):
        """
        Make DELETE call to remove object.
        :param payload:
        :return:
        """
        if '%s' in self.url:
            self._Connector__construct_url(payload['provider']['host'], payload['rel_url'])
        else:
            method = payload['method']
            if method not in ('POST', 'DELETE'):
                raise UnsupportedMethodException('method %s not supported' % method)
            elif method == 'POST':
                rsp = self.session.post(url=(self.url), headers=(payload.get('headers')), params=(payload.get('params')), data=(json.dumps(payload.get('body'))))
            else:
                rsp = self.session.delete(url=(self.url), headers=(payload.get('headers')), params=(payload.get('params')), data=(json.dumps(payload.get('body'))))
            status_code = rsp.status_code
            if status_code == 200:
                if len(rsp.content):
                    return rsp.json()
                    return '{"msg": "Successful"}'
                else:
                    pass
            raise APICallFailedException('API call failed. Msg :: ' + str(rsp.content.decode('utf-8')))