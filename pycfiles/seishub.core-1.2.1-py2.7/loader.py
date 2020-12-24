# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\loader.py
# Compiled at: 2010-12-23 17:42:44
import os, pkg_resources, sys
__all__ = [
 'ComponentLoader']

class ComponentLoader(object):
    """
    Load all plug-ins found on the given search path.
    """

    def __init__(self, env):
        self.env = env
        extra_path = env.config.get('seishub', 'plugins_dir')
        plugins_dir = os.path.join(env.config.path, 'plugins')
        search_path = [plugins_dir]
        if extra_path:
            search_path += list((extra_path,))
        self._loadEggs('seishub.plugins', search_path)

    def _loadEggs(self, entry_point, search_path):
        """
        Loader that loads SeisHub eggs from the search path and L{sys.path}.
        """
        self.env.log.debug('Looking for plug-ins ...')
        search_path += list(sys.path)
        distributions, errors = pkg_resources.working_set.find_plugins(pkg_resources.Environment(search_path))
        for d in distributions:
            if entry_point not in d.get_entry_map().keys():
                continue
            self.env.log.debug('Found egg %s ...' % d)
            pkg_resources.working_set.add(d)

        for dist, e in errors.iteritems():
            self.env.log.warn('Skipping egg "%s": %s' % (dist, e))

        for entry in pkg_resources.iter_entry_points(entry_point):
            self.env.log.debug('Initialize egg %s ...' % entry.module_name)
            try:
                entry.load()
            except Exception as e:
                self.env.log.warn('Skipping egg "%s": %s' % (entry.name, e))

        self.env.log.info('Plug-ins have been initialized.')