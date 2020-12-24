# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\env.py
# Compiled at: 2011-02-05 15:55:23
"""
The one class to rule them all.

Environment is the base class to handle configuration, XML catalog, database 
and logging access.
"""
from seishub.core.auth import AuthenticationManager
from seishub.core.config import Configuration, Option, _TRUE_VALUES, BoolOption
from seishub.core.core import ComponentManager
from seishub.core.db.manager import DatabaseManager
from seishub.core.defaults import DEFAULT_COMPONENTS, HTTP_PORT, WIN_DEBUG, BASH_START, BASH_STOP, BASH_DEBUG
from seishub.core.log import Logger
from seishub.core.packages.installer import PackageInstaller
from seishub.core.processor import ResourceTree
from seishub.core.util.loader import ComponentLoader
from seishub.core.xmldb.xmlcatalog import XmlCatalog
from twisted.application import service
from twisted.internet import defer
import os, sys, time, stat
from seishub.core.registry.registry import ComponentRegistry

class Environment(ComponentManager):
    """
    The one class to rule them all.
    
    Environment is the base class to handle configuration, XML catalog, 
    database and logging access.
    
    A SeisHub environment consists of:
        * a configuration handler env.config
        * a XML catalog handler env.catalog
        * a database handler env.db
        * a logging handler env.log
        * a package handler env.registry
        * a user management handler env.auth
    """
    Option('seishub', 'host', 'localhost', 'Default host of this server.')
    BoolOption('seishub', 'use_trash_folder', False, 'Mode deleted resources into a trash folder.')

    def __init__(self, path, application=None, config_file='seishub.ini', log_file='seishub.log', create=None):
        """
        Initialize the SeisHub environment.
        """
        self.app = application
        self._path = path
        if not sys.hexversion >= 33947648:
            print 'ERROR: SeisHub needs at least Python 2.6 or higher in ' + 'order to run.'
            exit()
        if not sys.hexversion <= 50331648:
            print 'ERROR: SeisHub is not yet compatible with Python 3.x.'
            exit()
        if create:
            self.create(path)
        self.startup_time = int(time.time())
        if isinstance(config_file, Configuration):
            self.config = config_file
        else:
            config_file = os.path.join(path, 'conf', config_file)
            self.config = Configuration(config_file)
        self.config.path = path
        self.config.hubs = {}
        self.log = Logger(self, log_file)
        self.initDefaultOptions()
        self.db = DatabaseManager(self)
        ComponentManager.__init__(self)
        self.compmgr = self
        self.initDefaultOptions()
        self.catalog = XmlCatalog(self)
        self.auth = AuthenticationManager(self)
        ComponentLoader(self)
        self.registry = ComponentRegistry(self)
        PackageInstaller.install(self)
        self.tree = ResourceTree(self)
        self.update()
        self.xslt_params = {'google_api_key': self.config.get('web', 'google_api_key', '')}
        if create:
            exit()

    def create(self, path):
        """
        Creates a new SeisHub environment.
        """
        if not os.path.exists(path):
            os.mkdir(path)
        print 'Creating new SeisHub instance in %s' % path
        os.mkdir(os.path.join(path, 'bin'))
        os.mkdir(os.path.join(path, 'conf'))
        os.mkdir(os.path.join(path, 'data'))
        os.mkdir(os.path.join(path, 'db'))
        os.mkdir(os.path.join(path, 'logs'))
        fh = open(os.path.join(path, 'bin', 'debug.bat'), 'wt')
        fh.write(WIN_DEBUG % (sys.executable, path))
        fh.close()
        fh = open(os.path.join(path, 'bin', 'debug.sh'), 'wt')
        fh.write(BASH_DEBUG % (sys.executable, path))
        fh.close()
        fh = open(os.path.join(path, 'bin', 'start.sh'), 'wt')
        fh.write(BASH_START % (sys.executable, path))
        fh.close()
        fh = open(os.path.join(path, 'bin', 'stop.sh'), 'wt')
        fh.write(BASH_STOP % path)
        fh.close()
        try:
            os.chmod(os.path.join(path, 'bin', 'debug.sh'), 484)
            os.chmod(os.path.join(path, 'bin', 'start.sh'), 484)
            os.chmod(os.path.join(path, 'bin', 'stop.sh'), 484)
        except:
            pass

    def getPackagePath(self):
        """
        Returns the absolute root path to the SeisHub module directory.
        """
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def getInstancePath(self):
        """
        Returns the absolute root path to the SeisHub instance directory.
        """
        return self._path

    def initDefaultOptions(self):
        """
        Initialize any not yet set default options in configuration file.
        """
        defaults = self.config.defaults()
        for section in defaults.keys():
            for name in defaults.get(section).keys():
                if self.config.has_site_option(section, name):
                    continue
                else:
                    value = defaults.get(section).get(name)
                    self.config.set(section, name, value)
                    self.log.info('Setting default value for [%s] %s = %s' % (
                     section, name, value))
                    self.config.save()

    def getRestUrl(self):
        """
        Returns the root URL of the REST pages.
        """
        rest_host = self.config.get('seishub', 'host') or 'localhost'
        rest_port = self.config.getint('web', 'http_port') or HTTP_PORT
        return 'http://' + rest_host + ':' + str(rest_port)

    def update(self):
        """
        General update method after enabling/disabling components.
        """
        self.registry.mappers.update()
        self.registry.formaters.update()
        self.registry.processor_indexes.update()
        self.tree.update()
        self.catalog.updateAllIndexViews()
        self.registry.sqlviews.update()

    @defer.inlineCallbacks
    def enableService(self, id):
        """
        Enable a service.
        """
        for srv in service.IServiceCollection(self.app):
            if srv.service_id == id:
                if srv.running:
                    self.log.info('Service %s already started.' % srv.name)
                    return
                self.config.set(srv.service_id, 'autostart', True)
                self.config.save()
                yield defer.maybeDeferred(srv.startService)
                self.log.info('Starting service %s.' % srv.name)

    @defer.inlineCallbacks
    def disableService(self, id):
        """
        Disable a service.
        """
        for srv in service.IServiceCollection(self.app):
            if srv.service_id == id:
                self.config.set(srv.service_id, 'autostart', False)
                self.config.save()
                yield defer.maybeDeferred(srv.stopService)
                self.log.info('Stopping service %s.' % srv.name)

    def enableComponent(self, component, update=True):
        """
        Enables a component.
        """
        module = sys.modules[component.__module__]
        fullname = module.__name__ + '.' + component.__name__
        if component not in self:
            self[component]
        self.enabled[component] = True
        self.config.set('components', fullname, 'enabled')
        self.config.save()
        if hasattr(component, 'package_id'):
            try:
                PackageInstaller.install(self, component.package_id)
            except Exception as e:
                self.disableComponent(component)
                return str(e)

        self.log.info('Enabling component %s' % fullname)
        if update:
            self.update()

    def disableComponent(self, component, update=True):
        """
        Disables a component.
        """
        module = sys.modules[component.__module__]
        fullname = module.__name__ + '.' + component.__name__
        if fullname in DEFAULT_COMPONENTS:
            return
        if component in self:
            del self[component]
        self.enabled[component] = False
        self.config.set('components', fullname, 'disabled')
        self.log.info('Disabling component %s' % fullname)
        self.config.save()
        PackageInstaller.cleanup(self)
        if update:
            self.update()

    def initComponent(self, component):
        """
        Initialize additional member variables for components.
        
        Every component activated through the `Environment` object gets a few
        member variables: `env` (the environment object), `config` (the
        environment configuration), `log` (a logger object), `db` (the 
        database handler), `catalog` (a XML catalog object), `registry` (a 
        package registry handler) and `auth` (a user management object).
        """
        component.env = self
        component.config = self.config
        component.log = self.log
        component.db = self.db
        component.catalog = self.catalog
        component.registry = self.registry
        component.auth = self.auth

    def isComponentEnabled(self, cls):
        """
        Implemented to only allow activation of components that are not
        disabled in the configuration.
        
        This is called by the `ComponentManager` base class when a component is
        about to be activated. If this method returns false, the component does
        not get activated.
        """
        if isinstance(cls, basestring):
            modulename = ('.').join(cls.split('.')[:-1])
            classname = cls
        else:
            modulename = cls.__module__
            classname = modulename + '.' + cls.__name__
        if classname in DEFAULT_COMPONENTS:
            return True
        if modulename in DEFAULT_COMPONENTS:
            return True
        rules = [ (name, value in _TRUE_VALUES) for name, value in self.config.options('components')
                ]
        rules = sorted(rules)
        for pattern, state in rules:
            if pattern == classname.lower():
                return state
            if pattern == modulename.lower():
                return state

        return False