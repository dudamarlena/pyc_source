# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/plugin.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2711 bytes
"""
Implements plugin related api.

To define a new plugin just subclass Plugin, like this.

class AuthPlugin(Plugin):
    pass

Then start creating subclasses of your new plugin.

class MyFancyAuth(AuthPlugin):
    capability = ['sign', 'vmac']

The actual interface is duck typed.
"""
import glob, imp, os.path

class Plugin(object):
    __doc__ = 'Base class for all plugins.'
    capability = []

    @classmethod
    def is_capable(cls, requested_capability):
        """Returns true if the requested capability is supported by this plugin
        """
        for c in requested_capability:
            if c not in cls.capability:
                return False

        return True


def get_plugin(cls, requested_capability=None):
    if not requested_capability:
        requested_capability = []
    result = []
    for handler in cls.__subclasses__():
        if handler.is_capable(requested_capability):
            result.append(handler)
            continue

    return result


def _import_module(filename):
    path, name = os.path.split(filename)
    name, ext = os.path.splitext(name)
    file, filename, data = imp.find_module(name, [path])
    try:
        return imp.load_module(name, file, filename, data)
    finally:
        if file:
            file.close()


_plugin_loaded = False

def load_plugins(config):
    global _plugin_loaded
    if _plugin_loaded:
        return
    _plugin_loaded = True
    if not config.has_option('Plugin', 'plugin_directory'):
        return
    directory = config.get('Plugin', 'plugin_directory')
    for file in glob.glob(os.path.join(directory, '*.py')):
        _import_module(file)