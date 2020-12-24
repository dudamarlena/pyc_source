# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/nctu_oauth/oauth.py
# Compiled at: 2016-08-30 12:37:15
import requests
from flask import redirect, session
OAUTH_URL = 'https://id.nctu.edu.tw'

class Oauth(object):

    def __init__(self, redirect_uri, client_id, client_secret):
        self.grant_type = 'authorization_code'
        self.code = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        return

    def authorize(self):
        get_code_url = OAUTH_URL + '/o/authorize/?client_id=' + self.client_id + '&scope=profile&response_type=code'
        return redirect(get_code_url)

    def get_token(self, code):
        self.code = code
        get_token_url = OAUTH_URL + '/o/token/'
        data = {'grant_type': 'authorization_code', 
           'code': self.code, 
           'client_id': self.client_id, 
           'client_secret': self.client_secret, 
           'redirect_uri': self.redirect_uri}
        access_token = requests.post(get_token_url, data=data).json().get('access_token', None)
        if access_token:
            session['nctu_token'] = access_token
            session['logged_in'] = True
            return True
        else:
            return False

    def get_profile(self):
        token = session.get('nctu_token')
        headers = {'Authorization': 'Bearer ' + token}
        get_profile_url = OAUTH_URL + '/api/profile/'
        data = requests.get(get_profile_url, headers=headers).json()
        return data