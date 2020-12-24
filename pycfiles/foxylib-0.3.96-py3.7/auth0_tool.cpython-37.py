# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/auth/auth0/auth0_tool.py
# Compiled at: 2020-01-21 01:42:50
# Size of source mod 2**32: 3074 bytes
from functools import wraps
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from flask import session, redirect

class Auth0Tool:

    class Config:
        CLIENT_ID = 'client_id'
        CLIENT_SECRET = 'client_secret'
        API_BASE_URL = 'api_base_url'
        SCOPE = 'scope'

    @classmethod
    def j_config2client_id(cls, j_config):
        return j_config[cls.Config.CLIENT_ID]

    @classmethod
    def j_config2client_secret(cls, j_config):
        return j_config[cls.Config.CLIENT_SECRET]

    @classmethod
    def j_config2api_base_url(cls, j_config):
        return j_config[cls.Config.API_BASE_URL]

    @classmethod
    def j_config2scope(cls, j_config):
        return j_config[cls.Config.SCOPE]

    @classmethod
    def app_config2auth0(cls, app, j_config):
        oauth = OAuth(app)
        base_url = cls.j_config2api_base_url(j_config)
        scope = cls.j_config2scope(j_config)
        access_token_url = '{}/oauth/token'.format(base_url)
        authorize_url = '{}/authorize'.format(base_url)
        auth0 = oauth.register('auth0',
          client_id=(cls.j_config2client_id(j_config)),
          client_secret=(cls.j_config2client_secret(j_config)),
          api_base_url=base_url,
          access_token_url=access_token_url,
          authorize_url=authorize_url,
          client_kwargs={'scope': scope})
        return auth0

    @classmethod
    def auth0_url2callback(cls, auth0, url_redirect):
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        session['jwt_payload'] = userinfo
        session['profile'] = {'user_id':userinfo['sub'], 
         'name':userinfo['name'], 
         'picture':userinfo['picture']}
        return redirect(url_redirect)

    @classmethod
    def auth0_callback_url2login(cls, auth0, callback_url):
        return auth0.authorize_redirect(redirect_uri=callback_url)

    @classmethod
    def requires_auth(cls, func=None, login_url=None):
        if login_url is None:
            login_url = '/'

        def wrapper(f):

            @wraps(f)
            def wrapped(*_, **__):
                if 'profile' not in session:
                    return redirect(login_url)
                return f(*_, **__)

            return wrapped

        if func:
            return wrapper(func)
        return wrapper