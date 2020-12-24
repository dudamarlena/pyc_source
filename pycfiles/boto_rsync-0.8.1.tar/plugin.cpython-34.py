# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/plugin.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2711 bytes
__doc__ = "\nImplements plugin related api.\n\nTo define a new plugin just subclass Plugin, like this.\n\nclass AuthPlugin(Plugin):\n    pass\n\nThen start creating subclasses of your new plugin.\n\nclass MyFancyAuth(AuthPlugin):\n    capability = ['sign', 'vmac']\n\nThe actual interface is duck typed.\n"
import glob, imp, os.path

class Plugin(object):
    """Plugin"""
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