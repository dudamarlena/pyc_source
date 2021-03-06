# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/lib/authent_middleware.py
# Compiled at: 2007-12-04 10:31:52
"""This is an example of multiple middleware components being setup at once in
such away that the authentication method used is dynamically selected at
runtime. What happens is that each authentication method is based an
``AuthSwitcher`` object which when a status response matching a code specified
in ``authkit.setup.intercept`` is intercepted, will perform a ``switch()``
check. If the check returns ``True`` then that particular ``AuthHandler`` will
be triggered. 

In this example the ``AuthSwitcher`` decides whether to trigger a particular
``AuthHandler`` based on the value of the ``authkit.authhandler`` key in
``environ`` and this is set when visiting the various paths such as
``/private_openid``, ``private_basic`` etc. Notice though that the form method
is setup with a ``Default`` ``AuthSwitcher`` whose ``switch()`` method always
returns ``True``. This means of the other ``AuthHandlers`` don't handle the
response, the from method's handler will. This is the case if you visit
``/private``.

Once the user is authenticated the ``UserSetter``s middleware sets the
``REMOTE_USER`` environ variable so that the user remains signed in. This means
that a user can authenticate with say digest authentication and when they visit
``/private_openid`` they will still be signed in, even if that wasn't the
method they used to authenticate.

Also, note that you are free to implement and use any ``AuthSwitcher`` you like
as long as it derives from ``AuthSwitcher`` so you could for example choose
which authentication method to show to the user based on their IP address.

The authentication details for each method in this example are:

Form: username2:password2 
Digest: test:test (or any username which is identical to the password)
Basic: test:test (or any username which is identical to the password)
OpenID: any valid openid (get one at myopenid.com for example)

Of course, everything is totally configurable.
"""
from setproxy import set_proxy
from authkit.authenticate import middleware, strip_base
from authproxy.lib.authkit_adapter.authenticate.open_id import OpenIDAuthHandler, OpenIDUserSetter, load_openid_config
from authproxy.lib.authkit_adapter.authenticate.form import FormAuthHandler, load_form_config
from authkit.authenticate.cookie import CookieUserSetter, load_cookie_config
from authproxy.lib.authkit_adapter.authenticate.basic import BasicAuthHandler, BasicUserSetter, load_basic_config
from authproxy.lib.authkit_adapter.authenticate.digest import DigestAuthHandler, DigestUserSetter, load_digest_config, digest_password
from authkit.authenticate.multi import MultiHandler, AuthSwitcher, status_checker
from authproxy.lib.authkit_adapter.authenticate import valid_password as basic_authenticate
from authproxy.lib.authkit_adapter.authenticate import digest_password as digest_authenticate
import logging
log = logging.getLogger('authproxy')

class LoadAuthkitUsers(object):
    """
           adapter authkit-0.4  a sqlalchemyManager
           charger environ authkit.users
    """

    def __init__(self, app, authkit_user_class):
        """
            @authkit_users : objet UsersFromDatabase api authkit 0.4
        """
        self.app = app
        self.user_api = authkit_user_class

    def __call__(self, environ, start_response):
        """  chargement user api authkit 0.4 dans environ[authkit.users]  """
        user_api = self.user_api(environ)
        environ['authkit.users'] = user_api
        return self.app(environ, start_response)


class EnvironKeyAuthSwitcher(AuthSwitcher):

    def __init__(self, method, key='authkit.authhandler'):
        self.method = method
        self.key = key

    def switch(self, environ, status, headers):
        if environ.has_key(self.key) and environ[self.key] == self.method:
            return True
        return False


class Default(AuthSwitcher):

    def switch(self, environ, status, headers):
        return True


def make_multi_middleware(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.'):
    log.debug('authent_middleware.make_multi_middleware(.,%s,...)' % str(auth_conf))
    authproxy_form_enable = auth_conf.get('authproxy.form.enable', True)
    authproxy_openid_enable = auth_conf.get('authproxy.openid.enable', True)
    authproxy_basic_enable = auth_conf.get('authproxy.basic.enable', False)
    authproxy_digest_enable = auth_conf.get('authproxy.digest.enable', False)
    authproxy_httpproxy_url = auth_conf.get('authproxy.httpproxy.url', None)
    if authproxy_httpproxy_url:
        set_proxy(authproxy_httpproxy_url)
        log.debug('authproxy set proxy http:%s' % authproxy_httpproxy_url)
    elif authproxy_openid_enable:
        log.warning('no proxy http to access internet')
        log.debug('openid generaly needs to access internet')
        log.debug('assumes openid can access to internet directly')
    else:
        log.debug('no proxy http')
    if authproxy_openid_enable:
        (app, oid_auth_params, oid_user_params) = load_openid_config(app, strip_base(auth_conf, 'openid.'))
    (app, form_auth_params, form_user_params) = load_form_config(app, strip_base(auth_conf, 'form.'))
    (app, cookie_auth_params, cookie_user_params) = load_cookie_config(app, strip_base(auth_conf, 'cookie.'))
    if authproxy_basic_enable:
        (app, basic_auth_params, basic_user_params) = load_basic_config(app, strip_base(auth_conf, 'basic.'))
    if authproxy_digest_enable:
        (app, digest_auth_params, digest_user_params) = load_digest_config(app, strip_base(auth_conf, 'digest.'))
    assert cookie_auth_params == None
    assert form_user_params == None
    app = MultiHandler(app)
    if authproxy_openid_enable:
        log.debug('authproxy enables openid authentication')
        app.add_method('openid', OpenIDAuthHandler, **oid_auth_params)
        app.add_checker('openid', EnvironKeyAuthSwitcher('openid'))
    if authproxy_basic_enable:
        log.debug('authproxy enables basic authentication')
        app.add_method('basic', BasicAuthHandler, **basic_auth_params)
        app.add_checker('basic', EnvironKeyAuthSwitcher('basic'))
    if authproxy_digest_enable:
        log.debug('authproxy enables digest authentication')
        app.add_method('digest', DigestAuthHandler, **digest_auth_params)
        app.add_checker('digest', EnvironKeyAuthSwitcher('digest'))
    log.debug('authproxy enables form authentication by default')
    app.add_method('form', FormAuthHandler, **form_auth_params)
    app.add_checker('form', Default())
    if authproxy_digest_enable:
        app = DigestUserSetter(app, **digest_user_params)
    if authproxy_basic_enable:
        app = BasicUserSetter(app, **basic_user_params)
    if authproxy_openid_enable:
        app = OpenIDUserSetter(app, **oid_user_params)
    app = CookieUserSetter(app, **cookie_user_params)
    return app


import authkit
from authproxy.model import UsersFromDatabase
authproxy_url = '/auth'
authproxy_policyurl = 'http://localhost:5000'
authproxy_realm = 'Test Realm'
authproxy_defaults = dict(authproxy_form_enable=True, authproxy_openid_enable=True, authproxy_cookie_enable=True, authproxy_basic_enable=False, authproxy_digest_enable=False, authproxy_url=authproxy_url, authproxy_httpproxy_url=None, cookie_secret='somesecret', cookie_signoutpath='%s/signout' % authproxy_url, openid_path_signedin='%s/private_openid' % authproxy_url, openid_store_type='file', openid_store_config='', openid_charset='UTF-8', openid_sreg_required='fullname,nickname,city,country', openid_sreg_optional='timezone,email', openid_sreg_policyurl='http://localhost:5000', form_charset='UTF-8', digest_realm='Test Realm', digest_authenticate_function=digest_authenticate, basic_realm='Test Realm', basic_authenticate_function=basic_authenticate, form_authenticate_user_type='WSGI')
authproxy_mandatories = dict()

def make_middleware(app, global_conf, app_conf, authproxy_conf={}):
    log.debug('athent_middleware.make_middleware(\nglobal_conf=%s,\napp_conf=%s\n' % (global_conf, app_conf))
    conf = authproxy_defaults
    for (k, v) in app_conf.items():
        for selector in ('authproxy.', 'authkit.'):
            if k.startswith(selector):
                if selector == 'authproxy.':
                    k = k.replace('.', '_')
                elif selector == 'authkit.':
                    k = k[len(selector):].replace('.', '_')
                conf[k] = v
                break

    conf.update(authproxy_conf)
    conf.update(authproxy_mandatories)
    for (k, v) in conf.items():
        try:
            if v.lower() == 'true':
                conf[k] = True
                continue
            if v.lower() == 'false':
                conf[k] = False
                continue
            if v.lower() == 'none':
                conf[k] = None
                continue
        except:
            continue

    log.debug('authproxy conf=%s', conf)
    if conf.get('authproxy_enable', True):
        log.info('authproxy enabled')
        app = authkit.authenticate.middleware(app, middleware=make_multi_middleware, **conf)
        if conf.get('form_authenticate_user_type', 'WSGI') == 'WSGI':
            log.debug('wsgi authkit loader activated')
            app = LoadAuthkitUsers(app, UsersFromDatabase)
    else:
        log.info('authproxy disabled')
    return app