# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/VerifyKit/__init__.py
# Compiled at: 2019-11-07 05:53:30
import requests, json

class Verify:
    server_key = None
    response_body = {}
    is_valid = None
    api_version = 'v1.0'
    api_url = 'https://api.verifykit.com/'

    def __init__(self, server_key):
        self.server_key = server_key

    def is_valid(self):
        return self.is_valid

    def response(self):
        return self.response_body

    def validation(self, session_id):
        headers = {'X-Vfk-Server-Key': self.server_key}
        try:
            response = requests.post(('{}{}/{}').format(self.api_url, self.api_version, 'result'), json={'sessionId': session_id}, headers=headers)
            if response.status_code == 200:
                self.is_valid = True
                self.response_body = json.loads(response.content)['result']
            else:
                self.is_valid = False
                response_body = response.json()['meta']
                self.response_body = {'status': False, 
                   'errorCode': response_body['errorCode'], 
                   'errorMessage': response_body['errorMessage'], 
                   'requestId': response_body['requestId']}
        except Exception as e:
            self.is_valid = False
            response_body = response.json()['meta']
            self.response_body = {'status': False, 
               'errorCode': response_body['errorCode'], 
               'errorMessage': response_body['errorMessage'], 
               'requestId': response_body['requestId']}