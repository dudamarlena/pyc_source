# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/providers/facebook.py
# Compiled at: 2015-11-01 17:30:22
import re, urllib
from xml.sax import saxutils as su
from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
import requests
from ..base import AccessTokenBase, AuthRequestBase
from ..exceptions import LoginPasswordError, AccountLocked, WrongRedirectUrl

class FacebookAuthRequest(AuthRequestBase):
    """
    Facebook authorized request class
    """
    provider = 'facebook'
    form_action_domain = 'https://m.facebook.com'
    login_url = 'https://m.facebook.com/login.php'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36', 
       'Upgrade-Insecure-Requests': 1, 
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
       'Accept-Charset': 'utf-8;q=0.7,*;q=0.3', 
       'Accept-Encoding': 'gzip,deflate,sdch', 
       'Accept-Language': 'en-US,en;q=0.8', 
       'Connection': 'keep-alive', 
       'Host': 'www.facebook.com'}
    account_locked_phrases = [
     'Ваш аккаунт временно заблокирован',
     'Мы заблокировали ваш аккаунт в связи с попыткой входа из незнакомого места. Пожалуйста, помогите нам подтвердить, что попытка входа была произведена вами.',
     'Your account is temporarily locked.']

    def add_data_credentials(self, data):
        data['email'] = self.username
        data['pass'] = self.password

    def authorize(self):
        """
        TODO: cover with tests for each condition
        """
        response = super(FacebookAuthRequest, self).authorize()
        if 'Cookies Required' in response.content:
            self.session.get(self.form_action_domain)
            response = super(FacebookAuthRequest, self).authorize()
            if 'Cookies Required' in response.content:
                raise Exception("Facebook 'Cookies required' error")
        if 'You are trying too often' in response.content:
            raise Exception("Facebook authorization request returns error 'You are trying too often'")
        if 'API Error Code: 191' in response.content:
            raise ImproperlyConfigured("You must specify URL '%s' in your facebook application settings" % self.redirect_uri)
        for account_locked_phrase in self.account_locked_phrases:
            if account_locked_phrase in response.content:
                raise AccountLocked("Facebook errored 'Your account is temporarily locked.'. Try to login via web browser")

        return response


class FacebookAccessToken(AccessTokenBase):
    provider = 'facebook'
    type = 'oauth2'
    authorize_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'https://google.com/404'
    auth_request_class = FacebookAuthRequest

    def authorization_get_request(self):
        response = super(FacebookAccessToken, self).authorization_get_request()
        bs = BeautifulSoup(response.content)
        if bs.find('title').text == 'Error':
            raise WrongRedirectUrl(bs.find('div').text)
        return response

    def authorization_post_request(self, *args, **kwargs):
        self.auth_request.session.get(self.auth_request.form_action_domain)
        return super(FacebookAccessToken, self).authorization_post_request(*args, **kwargs)

    def authorization_permissions_request(self, response):
        if 'Redirecting...' in response.content:
            matches = re.findall('<meta http-equiv="refresh" content="0;url=(.+)" /></head>', response.content)
            url = su.unescape(urllib.unquote(matches[0]))
            response = self.oauth.request(method='get', url=url, cookies=response.cookies, headers=self.auth_request.headers)
        return response

    def get_url_from_response(self, response):
        if response.status_code == 404 and 'code=' in response.url:
            return response.url
        else:
            return
            return