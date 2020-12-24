# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremydw/git/edu-buy-flow/lib/airlock/oauth.py
# Compiled at: 2015-03-25 02:47:28
from . import handlers
from . import users
from apiclient import discovery
from google.appengine.api import memcache
from oauth2client import appengine
from oauth2client import xsrfutil
import httplib2, json, logging

class OAuth2CallbackHandler(handlers.Handler):
    """Callback handler for oauth2 flow."""

    def get(self):
        error = self.request.get('error')
        if error:
            message = self.request.get('error_description', error)
            logging.error(message)
            self.response.out.write('Authorization request failed.')
            return
        else:
            self.decorator._create_flow(self)
            credentials = self.decorator.flow.step2_exchange(self.request.params)
            http = credentials.authorize(httplib2.Http(memcache))
            service = discovery.build('oauth2', 'v2', http=httplib2.Http(memcache))
            data = service.userinfo().v2().me().get().execute(http=http)
            auth_id = ('google:{}').format(data['id'])
            user = self.user_model.get_by_auth_id(auth_id)
            if user is None:
                nickname = data['email']
                data.pop('id', None)
                unique_properties = ['nickname', 'email']
                ok, user = self.user_model.create_user(auth_id, unique_properties=unique_properties, nickname=nickname, **data)
                if not ok:
                    logging.exception(('Invalid values: {}').format(user))
                    self.error(500, 'Error creating user.')
                    return
            self.auth.set_session({'user_id': auth_id}, remember=True)
            session_user = users.UserStub(self.session['sid'])
            redirect_uri = appengine._parse_state_value(str(self.request.get('state')), session_user)
            storage = self.decorator._storage_class(model=self.decorator._credentials_class, key_name=('user:{}').format(user.user_id()), property_name=self.decorator._credentials_property_name)
            storage.put(credentials)
            if self.decorator._token_response_param and credentials.token_response:
                resp = json.dumps(credentials.token_response)
                redirect_uri = appengine.util._add_query_parameter(redirect_uri, self.decorator._token_response_param, resp)
            self.redirect(redirect_uri)
            return


class SignOutHandler(handlers.Handler):

    def get(self):
        key = self.config['webapp2_extras.sessions']['secret_key']
        redirect_url = str(self.request.get('redirect'))
        if self.me is not None:
            token = str(self.request.get('token'))
            xsrfutil.validate_token(key, token, self.me.user_id(), action_id=redirect_url)
            self.auth.unset_session()
        self.redirect(redirect_url)
        return