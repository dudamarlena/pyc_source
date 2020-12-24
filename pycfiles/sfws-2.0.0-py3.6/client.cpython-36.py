# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfws/client.py
# Compiled at: 2020-04-21 14:36:24
# Size of source mod 2**32: 5285 bytes
import requests, sys, json, base64
from requests.auth import HTTPBasicAuth

class Client:
    auth_end_point = str('account.demandware.com/dw/oauth2/access_token')
    api_service = 'data_api'
    end_point = str('')
    end_point_request = str('')
    api_credentials = {'host':None, 
     'host_staging':None, 
     'client_id':None, 
     'client_secret':None, 
     'version':None}
    is_secure = False
    request_method = str('POST')
    api = None

    def __init__(self, api_credentials):
        self.api_credentials = api_credentials
        self.set_base_end_point()
        self.is_secure = bool(api_credentials['ssl_verify'])

    def set_api(self, api):
        self.api = api

    def do_OAuth(self):
        response = None
        basic = str(self.api_credentials['client_id']) + str(':') + str(self.api_credentials['client_secret'])
        basic = base64.b64encode(basic.encode())
        try:
            user = str(self.api_credentials['client_id'])
            password = str(self.api_credentials['client_secret'])
            data = []
            if self.api_service == 'data_api':
                data = [('grant_type', 'client_credentials')]
            else:
                data = [('grant_type', 'urn:demandware:params:oauth:grant-type:client-id:dwsid:dwsecuretoken')]
            if self.api_service == 'data_api':
                headers = {'Cache-Control':'no-cache',  'Content-Type':'application/x-www-form-urlencoded'}
            else:
                headers = {'Cache-Control':'no-cache',  'Content-Type':'application/x-www-form-urlencoded', 
                 'Authorization':'Basic bWlsYW4ucGFuaWNAb3NmLWNvbW1lcmNlLmNvbTpDYTlsIW5hMDExOmZYKUNrUjYybVI='}
            url = self.get_auth_end_point()
            print('enpoint *********')
            print(url)
            print('*****************')
            if self.api_service == 'data_api':
                response = requests.post(url=url, data=data, headers=headers, auth=(HTTPBasicAuth(user, password)))
            else:
                response = requests.post(url=url, data=data, headers=headers)
            response = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            exc_traceback = sys.exc_info()
            print(repr(e))

        return response

    def do_request(self, access_token, parameters={}):
        response = None
        headers = {'Authorization':'Bearer ' + str(access_token), 
         'Accept':'application/json', 
         'Content-Type':'application/json'}
        print(self.get_end_point())
        req = requests.Request((self.request_method), (self.get_end_point()), headers=headers, json=parameters)
        prepared = req.prepare()
        s = requests.Session()
        try:
            response = s.send(prepared, verify=(self.is_secure))
        except Exception as e:
            exc_traceback = sys.exc_info()
            print(repr(e))

        return response

    def set_base_end_point(self):
        self.end_point = self.api_credentials['host']
        return self.end_point

    def set_request_path(self, request_end_point, method):
        self.end_point_request = self.api + str(self.api_credentials['version']) + str('/') + str(request_end_point)
        self.request_method = method

    def get_end_point(self):
        if self.is_secure == False:
            return str('http://') + str(self.end_point) + str(self.end_point_request)
        else:
            return str('https://') + str(self.end_point) + str(self.end_point_request)

    def get_auth_end_point(self):
        if self.api_service == 'shop_api':
            self.auth_end_point = self.api_credentials['host'] + str('/dw/oauth2/access_token') + str('?client_id=') + str(self.api_credentials['client_id'])
        else:
            if self.is_secure == False:
                self.auth_end_point = str('http://') + self.auth_end_point
            else:
                self.auth_end_point = str('https://') + self.auth_end_point
        print('CLIENT')
        print(self.auth_end_point)
        return self.auth_end_point