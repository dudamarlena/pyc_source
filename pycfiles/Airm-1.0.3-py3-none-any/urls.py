# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremydw/git/edu-buy-flow/lib/airlock/urls.py
# Compiled at: 2015-03-19 18:52:38
import urllib
from oauth2client import xsrfutil

class AuthUrls(object):

    def __init__(self, handler):
        self.handler = handler

    def sign_in(self):
        """Returns a signed URL to use to kick off the oauth2 flow."""
        return self.handler.decorator.authorize_url()

    def sign_out(self, redirect_url=None):
        """Returns a signed URL to disassociate the ouath2 user from the session."""
        key = self.handler.app.config['webapp2_extras.sessions']['secret_key']
        if redirect_url is None:
            redirect_url = self.handler.request.url
        user_id = self.handler.me.user_id()
        token = xsrfutil.generate_token(key, user_id, action_id=redirect_url)
        return ('/_airlock/signout?{}').format(urllib.urlencode({'redirect': redirect_url, 
           'token': token}))