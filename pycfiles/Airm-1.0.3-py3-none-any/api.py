# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremydw/git/edu-buy-flow/lib/airlock/api.py
# Compiled at: 2015-03-24 04:51:26
from . import config as config_lib
from . import handlers
from . import errors
from protorpc import remote
from webapp2_extras import auth as webapp2_auth
import Cookie, os, webapp2
__all__ = [
 'Service']

class Service(remote.Service, handlers.BaseHandler):
    """Enables compatibility with handlers.BaseHandler."""
    admin_verifier = None

    @webapp2.cached_property
    def app(self):
        config = config_lib.get_config()
        return webapp2.WSGIApplication(config=config)

    @webapp2.cached_property
    def request(self):
        request = webapp2.Request(environ=dict(os.environ))
        request.app = self.app
        return request

    @webapp2.cached_property
    def auth(self):
        return webapp2_auth.get_auth(request=self.request)

    def require_xsrf_protection(self):
        if self._endpoints_user is not None:
            return
        headers = self.__request_state.headers
        header_token = headers.get('X-XSRF-Token')
        if 'X-XSRF-Token' not in headers:
            raise errors.MissingXsrfTokenError('Missing XSRF header token.')
        if self.config.get('use_xsrf_cookie', False):
            cookie = Cookie.SimpleCookie(headers.get('cookie', ''))
            cookie_name = self.config.get('xsrf_cookie_name', config_lib.Defaults.Xsrf.COOKIE_NAME)
            if cookie_name not in cookie:
                raise errors.MissingXsrfTokenError('Missing XSRF cookie token.')
            cookie_token = cookie.get(cookie_name).value
            if header_token != cookie_token:
                raise errors.XsrfTokenMismatchError('XSRF token mismatch.')
        if not self.me.validate_token(header_token):
            raise errors.BadXsrfTokenError('Invalid XSRF token.')
        return

    @staticmethod
    def xsrf_protected(method):

        def wrapped_func(*args, **kwargs):
            self = args[0]
            self.require_xsrf_protection()
            return method(*args, **kwargs)

        return wrapped_func