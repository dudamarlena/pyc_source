# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/config/environment.py
# Compiled at: 2010-07-05 00:40:53
"""Pylons environment configuration"""
import os
from os.path import join, isfile
import time, re
from mako.lookup import TemplateLookup
from pylons.error import handle_mako_error
from pylons import config
from pylons import request, response, session
from pylons.controllers.util import abort
from sqlalchemy import engine_from_config
from authkit.authorize.pylons_adaptors import authorized
from pylons.configuration import PylonsConfig
import zeta.lib.app_globals as app_globals, zeta.lib.helpers as h
from zeta.lib.cache import cachemanager
from zeta.lib.constants import *
from zeta.lib.error import ZetaError
from zeta.config.routing import *
from zeta.model import init_model, meta, create_models
from zeta.ccore import ComponentManager
from zeta.comp.environ import open_environment
from zeta.comp.system import SystemComponent
from zeta.auth.perm import init_pms, permissions
try:
    from pylons import tmpl_context as c
except ImportError:
    import pylons
    pylons.tmpl_context = {}
    from pylons import tmpl_context as c

dirname = os.path.dirname
dbversion = '1.1'
zetaversion = '0.7b1'
zetacreators = 'SKR Farms (P) Ltd'
pkg_path = dirname(dirname(dirname(__file__)))
root = join(pkg_path, 'zeta')
envpath = ''
paths = dict(root=root, controllers=join(root, 'controllers'), static_files='', templates=[
 join(root, 'templates-dojo')])
compmgr = None
tmplmoddir = None
tckfilters = []
websetupconfig = None

def do_paths(app_conf):
    """setup environment directories"""
    global envpath
    global paths
    if not envpath:
        envpath = app_conf.get('zeta.envpath', '')
        if not envpath:
            envpath = join(pkg_path, 'defenv')
            app_conf['zeta.envpath'] = envpath
        template_dir = app_conf.get('zeta.template_dir', '')
        public_dir = app_conf.get('zeta.public_dir', '')
        if template_dir:
            paths['templates'] = [
             template_dir]
        paths['static_files'] = public_dir or join(envpath, 'public')


def setup_sysentries_cfg(config):
    """After all the configuration (both app-wide and site-wide) options are
    parsed and setup, this function should be called to populate them into a
    dictionary, which can be eventually used to create, modify, validate
    system entries from System table in the DataBase.
    If the system table is already created, then the configuration will be
    overwritten by entries in the table."""
    if not meta.sysentries_cfg:
        meta.sysentries_cfg = {'product_name': config['pylons.package'], 'product_version': config['zetaversion'], 
           'database_version': config['dbversion'], 
           'envpath': config['zeta.envpath'], 
           'siteadmin': config['zeta.siteadmin'], 
           'sitename': config['zeta.sitename'], 
           'timezone': config['zeta.timezone'], 
           'unicode_encoding': config['zeta.unicode_encoding'], 
           'welcomestring': config['zeta.welcomestring'], 
           'specialtags': (', ').join(config['zeta.specialtags']), 
           'projteamtypes': (', ').join(config['zeta.projteamtypes']), 
           'ticketstatus': (', ').join(config['zeta.ticketstatus']), 
           'tickettypes': (', ').join(config['zeta.tickettypes']), 
           'ticketseverity': (', ').join(config['zeta.ticketseverity']), 
           'ticketresolv': (', ').join(config['zeta.ticketresolv']), 
           'reviewnatures': (', ').join(config['zeta.reviewnatures']), 
           'reviewactions': (', ').join(config['zeta.reviewactions']), 
           'vcstypes': (', ').join(config['zeta.vcstypes']), 
           'wikitypes': (', ').join(config['zeta.wikitypes']), 
           'def_wikitype': config['zeta.def_wikitype'], 
           'userrel_types': (', ').join(config['zeta.userrel_types']), 
           'strictauth': unicode(config.get('zeta.strictauth', 'False')), 
           'googlemaps': unicode(config.get('zeta.googlemaps', '')), 
           'userpanes': config['zeta.userpanes'], 
           'regrbyinvite': unicode(config.get('zeta.regrbyinvite', 'False')), 
           'invitebyall': unicode(config.get('zeta.invitebyall', 'False')), 
           'interzeta': '{}'}
    return meta.sysentries_cfg


def parseconfig(config, global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config`` object"""
    global compmgr
    global tmplmoddir
    config.init_app(global_conf, app_conf, package='zeta', paths=paths)
    if config.has_key('zetaversion'):
        return
    else:
        config['routes.map'] = make_map(config)
        config['pylons.app_globals'] = app_globals.Globals(config)
        config['pylons.h'] = h
        config['zeta.pkg_path'] = pkg_path
        config['zeta.envpath'] = envpath
        config['zeta.pageheader'] = config['zeta.pageheader'] == 'True'
        config['zeta.siteadmin'] = unicode(config['zeta.siteadmin'])
        config['pylons.package'] = unicode(config['pylons.package'])
        config['zeta.timezone'] = unicode(config['zeta.timezone'])
        config['zeta.unicode_encoding'] = unicode(config['zeta.unicode_encoding'])
        config['zeta.sitename'] = unicode(config['zeta.sitename'])
        config['zeta.envpath'] = unicode(config['zeta.envpath'])
        config['zeta.welcomestring'] = unicode(config['zeta.welcomestring'])
        config['zeta.userrel_types'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.userrel_types']))
        config['zeta.projteamtypes'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.projteamtypes']))
        config['zeta.ticketstatus'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.ticketstatus']))
        config['zeta.tickettypes'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.tickettypes']))
        config['zeta.ticketseverity'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.ticketseverity']))
        config['zeta.reviewnatures'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.reviewnatures']))
        config['zeta.reviewactions'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.reviewactions']))
        config['zeta.wikitypes'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.wikitypes']))
        config['zeta.vcstypes'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.vcstypes']))
        config['zeta.ticketresolv'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.ticketresolv']))
        config['zeta.specialtags'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.specialtags']))
        config['zeta.def_wikitype'] = unicode(config['zeta.def_wikitype'])
        config['zeta.userpanes'] = map(lambda x: unicode(x), h.parse_csv(config['zeta.userpanes']))
        config['dbversion'] = dbversion
        config['zetaversion'] = zetaversion
        if not config['zeta.mstnccodes']:
            config['zeta.mstnccodes'] = join(envpath, 'public', 'mstnccodes.json')
        if not config['zeta.tckccodes']:
            config['zeta.tckccodes'] = join(envpath, 'public', 'tckccodes.json')
        if not config.get('zeta.tckfilters', None):
            config['zeta.tckfilters'] = join(envpath, 'public', 'tckfilters.pyd')
        tmplmoddir = join(app_conf['cache_dir'], 'templates')
        config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=tmplmoddir, input_encoding='utf-8', output_encoding=config['zeta.unicode_encoding'], imports=[
         'from webhelpers.html import escape'], default_filters=[
         'escape'])
        config['cachemgr'] = cachemanager(envpath)
        compmgr = open_environment(config)
        config['compmgr'] = compmgr
        return config


def cleantmplmodules():
    """Clear Mako generated template modules that are cached"""
    cmd = 'rm -rf %s' % tmplmoddir
    os.system(cmd)


def check_versionconsistency(sysentries):
    """Check whether application versions match with database versions"""
    if 'zeta.testmode' not in config:
        if sysentries['product_version'] != zetaversion:
            errmsg = 'db : ( %s ), app : ( %s ), ' % (
             sysentries['product_version'], zetaversion)
            raise ZetaError('Inconsistent product version, ' + errmsg)
        if sysentries['database_version'] != dbversion:
            errmsg = 'db : ( %s ), app : ( %s ), ' % (
             sysentries['database_version'], dbversion)
            raise ZetaError('Inconsistent database version, ' + errmsg)


def load_environment(global_conf, app_conf, userscomp=None):
    """Configure the Pylons environment. Will be executed only once, when
    the application is started."""
    global tckfilters
    config = PylonsConfig()
    do_paths(app_conf)
    parseconfig(config, global_conf, app_conf)
    setup_sysentries_cfg(config)
    h.mstnccodes = open(config['zeta.mstnccodes']).read()
    h.tckccodes = open(config['zeta.tckccodes']).read()
    h.webanalytics = ''
    if isfile(config['zeta.webanalytics']):
        h.webanalytics = open(config['zeta.webanalytics']).read()
    try:
        tckfilters = eval(open(config['zeta.tckfilters']).read())
    except:
        tckfilters = []

    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)
    return config


def setup_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config`` object, will
    be executed when the application is setup"""
    config = PylonsConfig()
    do_paths(app_conf)
    parseconfig(config, global_conf, app_conf)
    setup_sysentries_cfg(config)
    return config


def setup_models(config, userscomp):
    """Initialize and setup database tables"""
    config['userscomp'] = userscomp
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)
    create_models(engine, config, sysentries_cfg=meta.sysentries_cfg, permissions=permissions)
    return config


starttime = 0

def beforecontrollers(environ=None):
    """Generic function to be called before all controller actions are called.
    """
    global starttime
    starttime = time.time()
    syscomp = SystemComponent(compmgr)
    c.sysentries = syscomp.get_sysentry()
    if environ and environ.get('authkit.cookie.error', False):
        errmsg = environ.get('authkit.cookie.timeout', False) and 'Cookie timeout' or 'Reason not known !'
        h.flash('%sBad Cookie : %s' % (ERROR_FLASH, errmsg))
        h.redirect_to(r_accounts, action='signin')
    environ = environ or request.environ
    userscomp = environ['authkit.users']
    check_versionconsistency(c.sysentries)
    config['userscomp'] = userscomp
    if not config.has_key('c'):
        config['c'] = c
    if 'REMOTE_USER' in environ:
        c.authusername = environ['REMOTE_USER']
        c.authuser = userscomp.get_user(c.authusername, attrload=[
         'userinfo'])
        c.myprojects = h.myprojects(c.authuser)
        c.authorized = True
    else:
        c.authusername = 'anonymous'
        c.authuser = userscomp.get_user(c.authusername)
        c.myprojects = []
        c.authorized = False
    if not environ.get('authkit.users'):
        raise no_authkit_users_in_environ
    init_pms()
    c.project = None
    c.prjlogo = None
    c.view = None
    c.jsonobj = None
    c.textobj = None
    c.title = ''
    c.sitelogo = config['zeta.sitelogo']
    authkit_cookie = request.cookies.get('authkit', '')
    if not authkit_cookie:
        session['breadcrumbs'] = []
    return


def aftercontrollers():
    """Generic function to be called after all the controller actions are
    called."""
    bd = session.get('breadcrumbs', [])
    if not c.view == 'js' and not c.jsonobj and c.title and c.title != '-Skip-':
        bd = filter(lambda x: x[0] != c.title, bd)
        bd.insert(0, (c.title, request.url))
        session['breadcrumbs'] = bd[:MAX_BREADCRUMBS]
    session.save()
    if config['debug']:
        print '************ %s' % request.url
        print time.time() - starttime
        print