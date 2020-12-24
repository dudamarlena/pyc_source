# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/bundlemanager.py
# Compiled at: 2007-12-02 16:26:58
from pkg_resources import Environment, working_set
from salamoia.h2o.decorators import lazymethod
from salamoia.h2o.logioni import Ione
from salamoia.h2o.config import Config
from salamoia.h2o.bundle import Bundle
__all__ = [
 'BundleManager']

class BundleManager(object):
    """
    The bundle manager keeps track of installed and active bundles
    """
    __module__ = __name__

    @classmethod
    @lazymethod
    def defaultManager(cls):
        """
        Returns the global bundle manager
        """
        return BundleManager()

    def __init__(self):
        self.bundles = {}
        self.searchPath = Config.defaultConfig().getpaths('paths', 'bundles', '/var/lib/salamoia/bundles:installed_bundles')
        Ione.log('Bundle search path', self.searchPath)

    def registerEgg(self, name, egg):
        """
        register a setuptools egg file, creating a Bundle for it
        """
        self.registerBundle(name, Bundle(egg))

    def registerBundle(self, name, bundle):
        """
        register a bundle.
        
        The bundle will be activated.
        """
        self.bundles[name] = bundle
        bundle.activate()

    def refresh(self):
        """
        Searches the bundle path for new bundles and register them
        """
        env = Environment(self.searchPath)
        (dists, errors) = working_set.find_plugins(env)
        for egg in dists:
            if not self.bundles.has_key(egg.key):
                try:
                    self.registerEgg(egg.key, egg)
                except:
                    Ione.exception('Error loading bundle %s', egg, traceback=True)


from salamoia.tests import *
runDocTests()