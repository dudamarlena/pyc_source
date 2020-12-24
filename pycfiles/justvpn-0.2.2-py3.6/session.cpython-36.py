# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/justvpn/session.py
# Compiled at: 2020-05-01 07:08:40
# Size of source mod 2**32: 2792 bytes
import requests, os, re
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from .util import encode_url

class JustVpnSession(requests.Session):
    _LOGIN_URL = 'https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi'
    _header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    def __init__(self, username, password):
        super().__init__()
        for key in self._header:
            self.headers[key] = self._header[key]

        self._username = str(username)
        self._password = str(password)

    def login(self):
        post_vals = {'btnSubmit':'登录',  'password':self._password, 
         'realm':'LDAP-REALM', 
         'tz_offset':'480', 
         'username':self._username}
        res = self.post((self._LOGIN_URL), data=post_vals)
        soup = BeautifulSoup(res.text, 'lxml')
        if soup.find('input', id='btnSubmit_6') != None:
            return False
        else:
            if soup.find('input', id='btnContinue') != None:
                formDataStr = soup.find('input', id='DSIDFormDataStr').get('value')
                postdata = {'btnContinue':'继续会话',  'FormDataStr':formDataStr}
                res = self.post((self._LOGIN_URL), data=postdata)
            return True

    def get(self, url, **kwargs):
        if 'is_encode' not in kwargs or kwargs['is_encode']:
            res = (super().get)(encode_url(url), verify=False, **kwargs)
        else:
            res = (super().get)(url, verify=False, **kwargs)
        soup = BeautifulSoup(res.text, 'lxml')
        form = soup.find('form', id='frmSSLConfirm_2')
        if form != None:
            inputs = form.find_all('input')[:-1]
            post_vals = dict()
            for field in inputs:
                post_vals[field.get('name')] = field.get('value')

            res = super().post('https://vpn.just.edu.cn/dana/home/invalidsslsite_confirm.cgi', data=post_vals,
              verify=False)
        return res

    def post(self, url, data=None, json=None, **kwargs):
        if 'is_encode' not in kwargs or kwargs['is_encode']:
            return (super().post)(encode_url(url), data, json, verify=False, **kwargs)
        else:
            return (super().post)(url, data, json, verify=False, **kwargs)