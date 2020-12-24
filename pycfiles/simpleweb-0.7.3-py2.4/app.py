# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/app.py
# Compiled at: 2007-01-10 11:07:05
import sys
from middleware import StaticMiddleware, AuthMiddleware, SimpleErrorMiddleware
import simpleweb.utils

class SimplewebApp(object):
    __module__ = __name__

    def __init__(self, urls, config):
        self.wsgiapp = _create_app(urls, config)

    def __call__(self, environ, start_response):
        return self.wsgiapp(environ, start_response)


class SimplewebReloadingApp(object):
    __module__ = __name__

    def __call__(self, environ, start_response):
        import simpleweb._urls, simpleweb.settings
        urls = simpleweb._urls
        config = simpleweb.settings.Config('config')
        wsgiapp = _create_app(urls, config)
        wsgiapp = SimpleErrorMiddleware(wsgiapp, config.enable_debug, msg='An error has occured.\nFor a detailed traceback, enable debugging in config.py.\n You can do this by setting <pre >enable_debug = True</pre>')
        return wsgiapp(environ, start_response)


def _create_app(url, config):
    try:
        sys.path.insert(0, '.')
        __import__('urls')
    except ImportError, e:
        simpleweb.utils.msg_err('Could not successfully import urls.py: %s' % e)
        sys.exit()

    app = url.geturls()
    app = StaticMiddleware(app, config.working_directory)
    if hasattr(config, 'auth_plugin'):
        app = AuthMiddleware(app, authuser_class=config.auth_plugin.authuser_class)
    if config.enable_sessions:
        try:
            from flup.middleware.session import DiskSessionStore, SessionMiddleware
            app = SessionMiddleware(DiskSessionStore(), app)
        except ImportError:
            pass

    return app