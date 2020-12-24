# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/config/middleware.py
# Compiled at: 2007-12-04 08:13:40
"""Pylons middleware initialization"""
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, StaticJavascripts
from pylons.wsgiapp import PylonsApp
from authproxy.config.environment import load_environment
from authproxy.model import setup_model
from sqlalchemymanager import SQLAlchemyManager
import urllib

def local_error_mapper(code, message, environ, global_conf=None, **kw):
    if environ.get('pylons.error_call'):
        return
    else:
        environ['pylons.error_call'] = True
    if global_conf is None:
        global_conf = {}
    codes = [
     401, 403, 404]
    if environ['PATH_INFO'].startswith('/wiki/'):
        codes.remove(404)
    if not asbool(global_conf.get('debug')):
        codes.append(500)
    if code in codes:
        url = '/error/document/?%s' % urllib.urlencode({'message': message, 'code': code})
        return url
    return


def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by
        another WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    load_environment(global_conf, app_conf)
    app = PylonsApp()
    from authproxy.lib import authent_middleware
    app = authent_middleware.make_middleware(app, global_conf, app_conf)
    sqlalchemy_conf = app_conf
    app = SQLAlchemyManager(app, sqlalchemy_conf, [setup_model])
    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, error_template=error_template, **config['pylons.errorware'])
        app = ErrorDocuments(app, global_conf, mapper=local_error_mapper, **app_conf)
    app = RegistryManager(app)
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    return app


if __name__ == '__main__':
    print 'start'
    app = None
    application_name = 'auth'
    app = authkit.authenticate.middleware(app, setup_method='form,cookie', cookie_secret='somesecret', cookie_signoutpath='/%s/signout' % application_name, form_authenticate_user_type=authkit.users.UsersFromString, form_authenticate_user_data='cocoon:cocoon:super writer reviewer editor admin\ncocoon.myopenid.com:none:super writer reviewer editor admin        \nadmin:cocoon:pylons writer reviewer editor admin\n')