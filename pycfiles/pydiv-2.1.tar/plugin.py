# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/plugin.py
# Compiled at: 2016-03-07 14:40:46
__doc__ = '\nA simple plugin system.\n\nInspiration:\n\n* http://martyalchin.com/2008/jan/10/simple-plugin-framework\n* https://pypi.python.org/pypi/pluginloader\n'
import os, pkg_resources as pkg
from six import add_metaclass
from .logger import log

class PluginLoader(object):

    def __init__(self):
        self.loading = []
        self.loaded = set()

    def add_path(self, path):
        """Add a path to the load list."""
        self.loading.append(('path', path))

    def add_entrypoint(self, group):
        """Add an entrypoint group to the load list."""
        self.loading.append(('entrypoint', group))

    def load(self):
        """Load all plugins."""
        for tag, name in self.loading:
            if tag == 'path':
                self.load_directory(name)
            elif tag == 'entrypoint':
                for entrypoint in pkg.iter_entry_points(name):
                    group = name + '.' + entrypoint.name
                    self.load_plugin(entrypoint, group)

    def load_plugin(self, entrypoint, group):
        if group not in self.loaded:
            try:
                log.info("loading plugin from entry point '%s'" % group)
                entrypoint.load()
            except Exception:
                log.exception('error loading %s (ignored)' % group)

            self.loaded.add(group)

    def load_file(self, filename, context=None):
        if filename not in self.loaded:
            log.info("loading plugins from file '%s'", filename)
            try:
                context = context or {}
                with open(filename) as (fp):
                    exec (fp.read(), context)
            except Exception:
                log.exception('error loading %s (ignored)' % filename)

            self.loaded.add(filename)

    def load_directory(self, path, context=None):
        if path not in self.loaded and os.path.isdir(path):
            log.info("loading plugins from directory '%s'", path)
            for filename in os.listdir(path):
                if filename.endswith('.py'):
                    fullpath = os.path.join(path, filename)
                    self.load_file(fullpath, context)

            self.loaded.add(path)


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = {}
        elif hasattr(cls, 'name') and cls.name is not None:
            log.info('registering %s plugin: %s', cls.category, cls.name)
            cls.plugins[(cls.category, cls.name)] = cls
        return


@add_metaclass(PluginMount)
class Plugin(object):
    name = None
    category = None
    description = 'no description'
    version = '0.1'
    author = 'unknown'
    package = None


def get_plugin(basecls, name):
    """Look up and return a plugin of a given type and name."""
    for cls in get_plugins(basecls):
        if name == cls.name:
            return cls


def get_plugins(basecls):
    """Yield all plugins of a given type."""
    for (name, category), cls in sorted(basecls.plugins.items()):
        if issubclass(cls, basecls):
            yield cls


loader = PluginLoader()