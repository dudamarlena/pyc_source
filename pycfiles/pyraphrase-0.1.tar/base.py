# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mareike/work/app/pyrap-dev/python3/pyrap/base.py
# Compiled at: 2017-12-01 10:02:05
__doc__ = '\nCreated on Aug 1, 2015\n\n@author: nyga\n'
import dnutils, sys, os
from dnutils.threads import ThreadInterrupt
import web
from dnutils import expose, first, logs
from .sessions import PyRAPSession, SessionCleanupThread
from web.webapi import notfound
from pyrap import locations
from pyrap import server
import urllib.parse
routes = ('/(.*)/(.*)', 'RequestDispatcher', '/(.*)', 'RequestDispatcher')
web.config.debug = False
debug = True
dnutils.logs.loggers({'/pyrap/session_cleanup': logs.newlogger(logs.console, level=logs.ERROR), 
   '/pyrap/http': logs.newlogger(logs.console, level=logs.DEBUG), 
   '/pyrap/main': logs.newlogger(logs.console, level=logs.INFO)})

class PyRAPServer(web.application):

    def run(self, port=8080, bindip='127.0.0.1', *middleware):
        logger = dnutils.getlogger('/pyrap/main')
        SessionCleanupThread(session).start()
        try:
            logger.info('starting pyrap server')
            for path, app in _registry.items():
                logger.info('http://%s:%s/%s/' % (bindip, port, app.config.path))

            server.runbasic(self.wsgifunc(*middleware), (bindip, port))
        except (ThreadInterrupt, KeyboardInterrupt):
            logger.info('received ctrl-c')

        logger.info('goodbye.')


class ApplicationRegistry(object):
    """
    Store for all PyRAP application managers.
    
    Every app that is being registered gets an :class:`ApplicationManager` 
    instance that is configured with the respective `config` dict.
    The :class:`ApplicationManager` instance unique for every application
    context, i.e. if you try to register two PyRap apps under the same
    path, PyRAP will raise an Exception.
    """

    def __init__(self):
        self.apps = {}
        self.items = self.apps.items

    def register(self, config):
        from .engine import ApplicationManager
        if config.path in self.apps:
            raise Exception('An application with the name "%s" is already running in context path "%s"' % (self.apps[config.path].name, config.path))
        mngr = ApplicationManager(config)
        self.apps[config.path] = mngr
        mngr._setup()

    def __getitem__(self, key):
        return self.apps.get(key)


_server = PyRAPServer(routes, globals())
web.config.session_parameters.timeout = 1800
session = PyRAPSession(_server)
session.server = _server
_registry = ApplicationRegistry()

def register_app(clazz, path, name, entrypoints, setup=None, default=None, theme=None, icon=None, requirejs=None, requirecss=None, rcpath='rwt-resources'):
    """
    Register a new PyRAP app.
    
    :param clazz:        the main class of the application of which a new instance
                         will be created by PyRAP for every user session.
                         
    :param path:         the path of the URL under which the application will be 
                         accessible on the server.
                         
    :param name:         the name of the app, which will be used as the page 
                         title in the browser.
                         
    :param entrypoints:  a dict that maps the name of an entrypoint to a function
                         that is executed in order to initialize a new session
                         of the app.
                         
    :param theme:        the path to a css file that specifies the theme that
                         is used for the app.
                         
    :param rcpath:       the subpath of the HTTP path under which resources are
                         made accessible.
                         
    :param setup:        pointer to a function that is called for initializing
                         the app. Here loading static contents and registering
                         resources can go, for instance.

    :param icon:         image path under which the application's icon can
                         be found.
    """
    config = web.Storage({'clazz': clazz, 'path': path, 
       'name': name, 
       'entrypoints': dict(entrypoints), 
       'theme': theme, 
       'rcpath': rcpath, 
       'setup': setup, 
       'default': default, 
       'icon': icon, 
       'requirejs': requirejs, 
       'requirecss': requirecss})
    _registry.register(config)


register = register_app

def run(bindip='127.0.0.1', port=8080, admintool=False):
    if admintool:
        sys.path.append(os.path.join(locations.pyrap_path, 'examples', 'pyrap-admin'))
        from admin import PyRAPAdmin
        register(clazz=PyRAPAdmin, path='admin', entrypoints={'start': PyRAPAdmin.main}, name='pyRAP Administration')
    _server.run(bindip=bindip, port=port)


class RequestDispatcher(object):
    """
    The low-level component and interface to the webpy server dispatching
    every HTTP request to the application-specific request handlers. 
    
    Parses every request for its path, query and payload and is then dispatched
    to the respective application runtime.
    """

    def GET(self, *args, **kwargs):
        return self.POST(*args, **kwargs)

    def POST(self, *args, **kwargs):
        query = dict([ (str(k), str(v)) for k, v in urllib.parse.parse_qsl(web.ctx.query[1:], keep_blank_values=True) ])
        content = web.data()
        args = list(map(str, args))
        if not args:
            raise notfound()
        if len(args) > 1:
            tail = args[0].split('/')
            args = tail + [args[(-1)]]
        app_context = first(args, str)
        app_runtime = _registry[app_context]
        if app_runtime is None:
            raise notfound()
        else:
            return app_runtime.handle_request(args[1:], query, content)
        return