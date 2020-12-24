# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremydw/git/airlock/airlock/handlers.py
# Compiled at: 2015-03-30 13:25:58
from . import config
from . import errors
from . import urls
from . import users
from oauth2client import appengine
from webapp2_extras import auth as webapp2_auth
from webapp2_extras import security
from webapp2_extras import sessions
import endpoints, logging, webapp2
__all__ = [
 'Handler']

class BaseHandler(object):

    @webapp2.cached_property
    def me(self):
        if self._endpoints_user is not None:
            return self.user_model.get_or_create_by_email(self._endpoints_user.email())
        else:
            user_dict = self.auth.get_user_by_session()
            if user_dict:
                user = self.user_model.get_by_auth_id(str(user_dict['user_id']))
                if user:
                    return user
            return self.user_model(session_id=str(self.session.get('sid')))

    @webapp2.cached_property
    def _endpoints_user(self):
        try:
            return endpoints.get_current_user()
        except endpoints.InvalidGetUserCall:
            return

        return

    @webapp2.cached_property
    def auth(self):
        return webapp2_auth.get_auth()

    @property
    def user_model(self):
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    @webapp2.cached_property
    def urls(self):
        return urls.AuthUrls(self)

    @webapp2.cached_property
    def config(self):
        return self.app.config

    @webapp2.cached_property
    def decorator(self):
        try:
            client_secrets_path = self.config['client_secrets_path']
        except KeyError:
            raise config.ConfigError('Missing: client_secrets_path')

        decorator = appengine.oauth2decorator_from_clientsecrets(client_secrets_path, scope=self.config.get('scopes', config.Defaults.OAUTH_SCOPES))
        decorator._callback_path = '/_airlock/oauth2callback'
        return decorator

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    def _apply_security_headers(self, headers):
        policies = self.config.get('policies', {})
        hsts_policy = policies.get('hsts', config.Defaults.Policies.HSTS)
        if self.request.scheme.lower() == 'https' and hsts_policy is not None:
            include_subdomains = bool(hsts_policy.get('includeSubdomains', False))
            subdomain = '; includeSubdomains' if include_subdomains else ''
            hsts_value = 'max-age=%d%s' % (int(hsts_policy.get('max_age')), subdomain)
            headers['Strict-Transport-Security'] = hsts_value
        frame_options_policy = policies.get('frame_options', config.Defaults.XFrameOptions.SAMEORIGIN)
        if frame_options_policy is not None:
            headers['X-Frame-Options'] = frame_options_policy
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['X-Content-Type-Options'] = 'nosniff'
        if 'csp' in policies and 'policy' in policies['csp']:
            csp_policy = policies['csp']
            policies = policies['csp']['policy']
            header_name = 'Content-Security-Policy'
            if csp_policy.get('report_only'):
                header_name = 'Content-Security-Policy-Report-Only'
            policy_items = []
            for key, vals in policies.iteritems():
                val = (' ').join(vals)
                policy_items.append(('{} {}').format(key, val))

            headers[header_name] = ('; ').join(policy_items)
        return headers

    def _apply_session_properties(self):
        if self.session.get('sid', None) is None:
            self.session['sid'] = security.generate_random_string(entropy=128)
        if self.me.registered:
            self.decorator.credentials = self.decorator._storage_class(self.decorator._credentials_class, None, self.decorator._credentials_property_name, user=self.me).get()
        else:
            self.decorator._create_flow(self)
            session_user = users.UserStub(self.session['sid'])
            self.decorator.flow.params['state'] = appengine._build_state_value(self, session_user)
        return

    def initialize(self, request, response):
        webapp2.RequestHandler.initialize(self, request, response)
        self._apply_security_headers(response.headers)
        self._apply_session_properties()

    def dispatch(self):
        """Wraps the dispatch method to add session support."""
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    def require_me(self):
        if not self.me.registered:
            raise errors.NotAuthorizedError('You must be logged in.')

    def require_registered(self):
        if not self.me.registered:
            raise errors.NotAuthorizedError('You must be logged in.')

    def require_admin(self, admin_verifier_func=None):
        if admin_verifier_func is None:
            admin_verifier_func = self.admin_verifier
        if not self.me.registered:
            raise errors.NotAuthorizedError('Not authorized.')
        if not admin_verifier_func(self.me.email):
            logging.error(('User is forbidden: {}').format(self.me))
            raise errors.ForbiddenError('Forbidden.')
        return

    @staticmethod
    def admin_required(admin_func):

        def decorator(method):

            def wrapped_func(*args, **kwargs):
                self = args[0]
                self.require_admin()
                return method(*args, **kwargs)

            return wrapped_func

        return decorator

    @staticmethod
    def me_required(method):

        def wrapped_func(*args, **kwargs):
            self = args[0]
            self.require_me()
            return method(*args, **kwargs)

        return wrapped_func


class Handler(BaseHandler, webapp2.RequestHandler):
    """A request handler that supports webapp2 sessions."""