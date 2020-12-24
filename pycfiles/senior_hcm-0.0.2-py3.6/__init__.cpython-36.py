# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/senior_hcm/__init__.py
# Compiled at: 2019-04-07 19:00:03
# Size of source mod 2**32: 1331 bytes
import json, requests

class SeniorHcm:
    API_ROOT_URL = 'https://hcm-api.senior.com.br/frontend-api/'
    LOGIN_URL = API_ROOT_URL + 'login'
    RECENTS_PAYROLLS_URL = API_ROOT_URL + 'payrollregister/recents/{user_id}'

    def __init__(self, email, password):
        self._session = requests.Session()
        self.login(email=email, password=password)

    def login(self, email, password):
        data = {'email':email, 
         'password':password}
        headers = {'content-type': 'application/json;charset=UTF-8'}
        response = self._session.post((self.LOGIN_URL), data=(json.dumps(data)),
          headers=headers)
        if response.status_code != 200:
            message = '{} ({})'.format(response.reason, response.status_code)
            raise LoginError(f"Erro ao autenticar {message}")
        self.set_user_id(response.json())

    def set_user_id(self, response):
        self.user_id = response['session']['employees'][0]['id']

    def get_recent_payrolls(self):
        url = self.RECENTS_PAYROLLS_URL.format(user_id=(self.user_id))
        response = self._session.get(url)
        return response.json()

    def get_last_payroll(self):
        return self.get_recent_payrolls()['list'][0]


class LoginError(Exception):
    pass