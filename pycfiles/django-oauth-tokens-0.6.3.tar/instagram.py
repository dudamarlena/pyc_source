# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/providers/instagram.py
# Compiled at: 2016-01-18 10:51:50
import re
from bs4 import BeautifulSoup
import simplejson as json
from ..base import AccessTokenBase, AuthRequestBase, log
from ..exceptions import LoginPasswordError, AccountLocked, WrongRedirectUrl, RedirectUriError

class InstagramAuthRequest(AuthRequestBase):
    """
    Instagram authorized request class
    """
    provider = 'instagram'
    form_action = 'https://www.instagram.com/accounts/login/ajax/'
    form_action_domain = 'https://www.instagram.com'
    login_url = form_action_domain
    headers = {'Accept': '*/*', 
       'Origin': 'https://www.instagram.com', 
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
       'Referer': 'https://www.instagram.com/', 
       'X-Instagram-AJAX': 1, 
       'Accept-Encoding': 'gzip, deflate', 
       'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6'}

    def add_data_credentials(self, data):
        data['username'] = self.username
        data['password'] = self.password

    def get_form_data_from_content(self, content, force_classic_login=False, **kwargs):
        if force_classic_login:
            return super(InstagramAuthRequest, self).get_form_data_from_content(content)
        tokens = re.findall('"csrf_token"\\:"([^"]+)"', content)
        if len(tokens) == 0:
            raise Exception('No any CSRF token in source of login page')
        self.headers['X-CSRFToken'] = tokens[0]
        data = {}
        self.add_data_credentials(data)
        return ('post', self.form_action, data)


class InstagramAccessToken(AccessTokenBase):
    provider = 'instagram'
    type = 'oauth2'
    authorize_url = 'https://api.instagram.com/oauth/authorize'
    access_token_url = 'https://api.instagram.com/oauth/access_token'
    redirect_uri = 'http://instagram.com'
    auth_request_class = InstagramAuthRequest

    def authorization_permissions_request(self, response):
        if response.url[:72] == 'https://www.instagram.com/oauth/authorize?response_type=token&client_id=':
            bs = BeautifulSoup(response.content)
            form = self.auth_request.get_form_from_bs_content(bs)
            method, action, data = self.auth_request.get_form_data(form)
            del data['username']
            del data['password']
            response = self.auth_request.session.post(action, data, headers=self.auth_request.headers)
        return response

    def process_authorization_response(self, response):
        import ipdb
        ipdb.set_trace()
        if response.url[:33] == 'https://www.instagram.com/?state=':
            for resp in response.history:
                if 'access_token=' in resp.url:
                    response = resp

        return super(InstagramAccessToken, self).process_authorization_response(response)

    def authorization_get_request(self):
        response = super(InstagramAccessToken, self).authorization_get_request()
        if response.status_code == 403:
            response_json = json.loads(response.content)
            if response_json['status'] == 'fail':
                authorization_url = 'https://www.instagram.com' + response_json['redirect_url']
                response = self.auth_request.session.get(url=authorization_url, headers=self.auth_request.headers)
        return response

    def authorization_post_request(self, response):
        method, action, data = self.auth_request.get_form_data_from_content(response.content, force_classic_login=True)
        response = getattr(self.auth_request.session, method)(url=action, headers=self.auth_request.headers, data=data)
        if response.status_code == 400:
            response_json = json.loads(response.content)
            raise RedirectUriError('Code %(code)s. %(error_type)s: %(error_message)s' % response_json)
        return response

    def get_authorization_url(self):
        authorization_url = super(InstagramAccessToken, self).get_authorization_url()
        return authorization_url.replace('response_type=code', 'response_type=token')

    def get_url_from_response(self, response):
        return response.url.split('access_token=')[1]

    def fetch_token(self, access_token):
        return {'access_token': access_token}