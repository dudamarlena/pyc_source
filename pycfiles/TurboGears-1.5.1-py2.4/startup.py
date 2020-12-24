# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\startup.py
# Compiled at: 2011-11-20 06:54:09
"""Things to do when the TurboGears server is started."""
__all__ = [
 'call_on_startup', 'call_on_shutdown', 'reloader_thread', 'webpath', 'start_bonjour', 'stop_bonjour', 'start_server', 'start_turbogears', 'stop_turbogears']
import atexit, logging, os, signal, sys
from os.path import abspath, exists
import pkg_resources, cherrypy
pkg_resources.require('TurboGears')
from turbogears import config, database, scheduler, view
from turbogears.visit.api import VisitTool
from turbogears.identity.exceptions import IdentityConfigurationException
from turbogears.identity.base import verify_identity_status
from turbogears.database import hub_registry
from turbogears.dispatchers import VirtualPathDispatcher
from turbogears.hooks import NestedVariablesHook
log = logging.getLogger('turbogears.startup')
dns_sd_pid = None
call_on_startup = []
call_on_shutdown = []
webpath = ''
started = False

def start_bonjour(package=None):
    """Register the TurboGears server with Apple's Bonjour framework.

    Currently only Unix-like systems are supported where either the 'avahi'
    daemon (Linux etc.) is available or the 'dns-sd' program (Mac OS X).

    """
    global dns_sd_pid
    if dns_sd_pid:
        return
    if sys.platform in ('win32', 'os2'):
        dns_sd_pid = -1
        return
    if not package:
        app = cherrypy.tree.apps.get('')
        if not app:
            return
        package = app.root.__module__
        package = package.split('.', 1)[0]
    host = config.get('server.socket_host', '0.0.0.0')
    port = str(config.get('server.socket_port'))
    env = config.get('environment') or 'development'
    name = '%s:%s' % (package, env)
    typ = '_http._tcp'
    cmds = [('/usr/bin/avahi-publish-service', ['-H', host, name, typ, port]), ('/usr/bin/dns-sd', ['-R', name, typ, '.' + host, port, 'path=/'])]
    for (cmd, args) in cmds:
        if exists(cmd):
            dns_sd_pid = os.spawnv(os.P_NOWAIT, cmd, [cmd] + args)
            atexit.register(stop_bonjour)
            break
    else:
        dns_sd_pid = -1


def stop_bonjour():
    """Stop the Bonjour publishing daemon if it is running."""
    if not dns_sd_pid or dns_sd_pid < 0:
        return
    try:
        os.kill(dns_sd_pid, signal.SIGTERM)
    except OSError:
        pass


def config_static():
    """Configure serving static content used by TurboGears."""
    config.update({'/tg_static': {'tools.staticdir.on': True, 'tools.staticdir.dir': abspath(pkg_resources.resource_filename(__name__, 'static'))}})
    config.update({'/tg_js': {'tools.staticdir.on': True, 'tools.staticdir.dir': abspath(pkg_resources.resource_filename(__name__, 'static/js'))}})


def config_root():
    """Configure the encoding and virtual path for the root controller."""
    global webpath
    encoding = config.get('genshi.default_encoding', config.get('kid.encoding', 'utf-8'))
    config.update({'/': {'tools.decode.on': True, 'tools.decode.encoding': encoding, 'tools.encode.on': False, 'tools.encode.encoding': encoding, 'tools.encode.text_only': False, 'tools.encode.add_charset': False}})
    webpath = config.get('server.webpath') or ''
    if webpath:
        webpath = webpath.strip('/')
        if webpath:
            webpath = '/' + webpath
        config.update({'server.webpath': webpath})
        if webpath:
            config.update({'/': {'request.dispatch': VirtualPathDispatcher(config.get('request.dispatch'), webpath)}})
    if config.get('tg.fancy_exception', False):
        from paste import evalexception
        config.update({'request.throw_errors': True, '/': {'wsgi.pipeline': [('evalexc', evalexception.EvalException)], 'wsgi.evalexc.global_conf': {}, 'wsgi.evalexc.xmlhttp_key': '_xml'}})


def start_turbogears():
    """Handles TurboGears tasks when the CherryPy server starts.

    This performs the following initialization tasks (in given order):

    * Loads the template engines and the base templates.
    * Turns off CherryPy access and error logging to screen since
      it disrupts with our own logging configuration. You can use
      the qualnames cherrypy.access and cherrypy.error for these messages.
    * Adds a static tool for TurboGears's static files (URL '/tg_static').
    * Adds a static tool for TurboGears's JavaScript files (URL '/tg_js').
    * Adds a tool for decoding request parameters to Unicode.
    * Adds a virtual path dispatcher if enabled in the configuration.
    * Adds CherryPy tools and hooks for visit tracking, identity,
      database and decoding parameters into nested dictionaries.
    * Registers the server with the Bonjour framework, if available.
    * Calls 'turbogears.database.bind_metadata' when using SQLAlchemy.
    * Loads all turbogears.extensions entry points and calls their
      'start_extension' method.
    * Calls the callables registered in 'turbogears.call_on_startup'.
    * Starts the TurboGears scheduler if enabled in the configuration.

    """
    global started
    if started:
        log.info('TurboGears has already been started.')
        return
    log.info('Starting TurboGears...')
    log.info('Loading template engines...')
    view.load_engines()
    view.loadBaseTemplates()
    log.info('Adding CherryPy tools, hooks and dispatchers...')
    config_static()
    config_root()
    hooks = cherrypy.request.hooks
    cherrypy.request.original_hooks = hooks.copy()
    hooks.attach('before_finalize', verify_identity_status)
    hooks.attach('on_end_resource', database.EndTransactions)
    hooks.attach('before_handler', NestedVariablesHook, priority=64)
    if config.get('visit.on', False):
        cherrypy.tools.visit = cherrypy.Tool('before_handler', VisitTool(), priority=62)
    bonjour = config.get('tg.bonjour', None)
    env = config.get('environment') or 'development'
    if bonjour or env == 'development':
        log.info('Starting the Bonjour service...')
        start_bonjour(bonjour)
    if config.get('sqlalchemy.dburi'):
        log.info('Binding metadata for SQLAlchemy...')
        database.bind_metadata()
    extensions = pkg_resources.iter_entry_points('turbogears.extensions')
    for entrypoint in extensions:
        log.info('Starting TurboGears extension %s...' % entrypoint)
        try:
            ext = entrypoint.load()
        except Exception, e:
            log.exception('Error loading TurboGears extension plugin %s: %s', entrypoint, e)
            continue

        if hasattr(ext, 'start_extension'):
            try:
                ext.start_extension()
            except Exception, e:
                log.exception('Error starting TurboGears extension %s: %s', entrypoint, e)
                if isinstance(e, IdentityConfigurationException):
                    raise

    if call_on_startup:
        log.info('Running the registered startup functions...')
        for startup_function in call_on_startup:
            startup_function()

    if config.get('tg.scheduler', False):
        log.info('Starting the scheduler...')
        scheduler.start_scheduler()
    started = True
    log.info('TurboGears has been started.')
    return


def stop_turbogears():
    """Handles TurboGears tasks when the CherryPy server stops.

    Ends all open database transactions, shuts down all extensions,
    calls user provided shutdown functions and stops the scheduler.

    """
    global started
    if not started:
        log.info('TurboGears has already been stopped.')
        return
    log.info('Stopping TurboGears...')
    if config.get('tg.scheduler', False):
        log.info('Stopping the scheduler...')
        scheduler.stop_scheduler()
    if call_on_shutdown:
        log.info('Running the registered shutdown functions...')
        for shutdown_function in call_on_shutdown:
            shutdown_function()

    extensions = pkg_resources.iter_entry_points('turbogears.extensions')
    for entrypoint in extensions:
        log.info('Stopping TurboGears extension %s' % entrypoint)
        try:
            ext = entrypoint.load()
        except Exception, e:
            log.exception("Error loading TurboGears extension plugin '%s': %s", entrypoint, e)
            continue

        if hasattr(ext, 'shutdown_extension'):
            try:
                ext.shutdown_extension()
            except Exception, e:
                log.exception("Error shutting down TurboGears extension '%s': %s", entrypoint, e)

    if hub_registry:
        log.info('Ending all registered database hubs...')
        for hub in hub_registry:
            hub.end()

        hub_registry.clear()
    log.info('Stopping the Bonjour service...')
    stop_bonjour()
    log.info('Removing additional CherryPy hooks...')
    try:
        cherrypy.request.hooks = cherrypy.request.original_hooks
    except AttributeError:
        log.debug('CherryPy hooks could not be restored.')

    started = False
    log.info('TurboGears has been stopped.')


def start_server(root):
    """Start the CherryPy Server."""
    if started:
        log.info('The server has already been started.')
        return
    app = cherrypy.tree.mount(root, config=config.app)
    config.update({'log.screen': False})
    embedded = config.get('environment') == 'embedded'
    if config.get('engine.start', not embedded):
        cherrypy.engine.start()
        if config.get('engine.block', not embedded):
            cherrypy.engine.block()
    else:
        start_turbogears()
        atexit.register(stop_turbogears)
    return app


cherrypy.engine.subscribe('start', start_turbogears)
cherrypy.engine.subscribe('stop', stop_turbogears)