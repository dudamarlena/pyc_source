# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\nmdev\src\branches\loyalty\evasion-web\evasion\web\config\environment.py
# Compiled at: 2010-06-23 06:03:00
"""Pylons environment configuration"""
import os, pprint, logging
from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
import evasion.web.lib.app_globals as app_globals, evasion.web.lib.helpers
from evasion.web.config.routing import make_map

def get_log():
    return logging.getLogger('evasion.web.config.environment')


def default_middleware(app, global_conf, app_conf, middleware_list):
    """
    Add the default pylons Routing/Session/Cache Middleware.
    """
    from routes.middleware import RoutesMiddleware
    from beaker.middleware import CacheMiddleware, SessionMiddleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    return app


def default_auth(app, global_conf, app_conf, middleware_list):
    """
    Add the default evasion file based authentification.
    """
    from evasion.web.config.repozewhomid import add_auth
    sitename = app_conf.get('sitename', '')
    sessionname = app_conf.get('beaker.session.key')
    sessionsecret = app_conf.get('beaker.session.secret')
    groupfile = app_conf.get('groupfile', '')
    passwordfile = app_conf.get('passwordfile', '')
    permissionfile = app_conf.get('permissionfile', '')
    app = add_auth(app, sitename, sessionname, sessionsecret, passwordfile, groupfile, permissionfile)
    return app


def no_modules_routes(map, controller_list, static_dir_list, template_list):
    """If there are no routes present this will add a default page to tell this.
    """
    if not map._routenames:
        get_log().warn('No modules loaded or no routes configured! Adding defaults.')
        base = 'evasion.web.controllers.%s'
        map.connect('root', '/', controller=base % 'root', action='index')
        from evasion.web import public as static
        static_dir_list.append(os.path.abspath(static.__path__[0]))
        from evasion.web import templates
        template_list.append(os.path.abspath(templates.__path__[0]))
        from evasion.web import controllers
        controller_list.append(os.path.abspath(controllers.__path__[0]))
    return map


def load_environment(global_conf, app_conf, websetup=False):
    """Configure the Pylons environment via the ``pylons.config``
    object

    :returns: return set up recovered which will be used
    used in websetup.py or middleware.py
    
        dict(
            loaded_modules = [ ... ],
            setup_app_list = [ ..setup_app function list..],
            middleware_list = [ ..functions like default_middleware or default_auth.. ],
            model_manager = model_manager,
        )

    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    controller_list = []
    template_list = []
    static_dir_list = []
    setup_app_list = []
    loaded_modules = []
    middleware_list = []
    enable_default_middleware = app_conf.get('enable_default_middleware', 'true')
    if enable_default_middleware.lower() == 'true':
        get_log().info('load_environment: enabling default middleware (enable_default_middleware = true).')
        middleware_list.append(default_middleware)
    else:
        get_log().warn('load_environment: default middleware disabled (enable_default_middleware = false).')
    enable_default_auth = app_conf.get('enable_default_auth', 'false')
    if enable_default_auth.lower() == 'true':
        get_log().info('load_environment: enabling default auth middleware (enable_default_auth = true).')
        middleware_list.append(default_auth)
    else:
        get_log().warn('load_environment: default auth middleware disabled (enable_default_auth = false).')
    model_manager = None
    map = make_map()
    g = app_globals.Globals()
    loaded_modules = app_conf.get('web_modules', 'evasion.web')
    loaded_modules = [ m for m in loaded_modules.split(',') if m ]
    get_log().info("load_environment: director evasion.web modules '%s'." % loaded_modules)
    module_rdicts = []
    for module in loaded_modules:
        try:
            get_log().info("load_environment: loading module '%s'." % module)
            importmod = module
            fromlist = module.split('.')
            m = __import__(importmod, fromlist=fromlist, level=0)
        except ImportError, e:
            get_log().error("load_environment: unable to load module '%s'." % module)
        else:
            try:
                rdict = m.configure(map, global_conf, app_conf, websetup)
                if 'controllers' in rdict and rdict['controllers']:
                    c = rdict['controllers']
                    if type(c) == type([]) or type(c) == type((0, )):
                        for p in rdict['controllers']:
                            controller_list.append(p)

                    else:
                        controller_list.append(c)
                if 'static' in rdict and rdict['static']:
                    c = rdict['static']
                    if type(c) == type([]) or type(c) == type((0, )):
                        for p in rdict['static']:
                            static_dir_list.append(p)

                    else:
                        static_dir_list.append(rdict['static'])
                if 'templates' in rdict and rdict['templates']:
                    c = rdict['templates']
                    if type(c) == type([]) or type(c) == type((0, )):
                        for p in rdict['templates']:
                            template_list.append(p)

                    else:
                        template_list.append(rdict['templates'])
                if 'map' in rdict and rdict['map']:
                    map = rdict['map']
                if 'middleware' in rdict and rdict['middleware']:
                    get_log().debug('load_environment: appending middleware to list: %s' % rdict['middleware'])
                    middleware_list.append(rdict['middleware'])
                if 'g' in rdict and rdict['g']:
                    g.__dict__[module] = rdict['g']
                if 'setup_app' in rdict and rdict['setup_app']:
                    get_log().debug('load_environment: appending to setup app list: %s' % rdict['setup_app'])
                    setup_app_list.append(rdict['setup_app'])
                if 'modelmanager' in rdict and rdict['modelmanager']:
                    if model_manager:
                        msg = "The model manager is set and the module '%s' is trying to replace!" % rdict['name']
                        get_log().error('load_environment: %s' % msg)
                        raise ValueError(msg)
                    else:
                        model_manager = rdict['modelmanager']
                        get_log().debug('load_environment: ModelManager instance set up: %s' % model_manager)
                if 'model' in rdict and rdict['model']:
                    if model_manager:
                        model_manager.addModel(rdict['model'])
                    else:
                        msg = "The module '%s' provides a model, however no ModelManager has been set by any module so far!" % rdict['name']
                        get_log().error('load_environment: %s' % msg)
                        raise ValueError(msg)
                module_rdicts.append((module, rdict))
                get_log().debug('load_environment: configure() returned:\n%s\n' % pprint.pformat(rdict))
            except SystemExit, e:
                raise
            except:
                get_log().exception("load_environment: module '%s' configuration error - " % module)

    map = no_modules_routes(map, controller_list, static_dir_list, template_list)
    config['routes.map'] = map
    paths = dict(root=root, controllers=controller_list, static_files=static_dir_list, templates=template_list)
    config.init_app(global_conf, app_conf, package='evasion.web', paths=paths)
    config['routes.map'] = map
    g.modules = loaded_modules
    config['pylons.app_globals'] = g
    config['pylons.h'] = evasion.web.lib.helpers
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', output_encoding='utf-8', default_filters=[
     'escape'], imports=[
     'from webhelpers.html import escape'])
    config['evasion.web.modules'] = {}
    for (module, rdict) in module_rdicts:
        kind = rdict['kind']
        m = config['evasion.web.modules'].get(kind, dict(kind=kind, modules=[]))
        m['modules'].append(dict(module=module, name=rdict['name'], desc=rdict['desc'], setup=rdict))
        config['evasion.web.modules'][kind] = m

    config['evasion.web.modelmanager'] = model_manager
    if model_manager:
        get_log().info('load_environment: calling model manager init.')
        model_manager.dbsetup = websetup
        model_manager.init()
    return dict(loaded_modules=loaded_modules, setup_app_list=setup_app_list, middleware_list=middleware_list, model_manager=model_manager)