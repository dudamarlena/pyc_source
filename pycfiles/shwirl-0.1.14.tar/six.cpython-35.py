# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/ext/six.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 3453 bytes
"""
Handle loading six package from system or from the bundled copy
"""
try:
    import importlib
except ImportError:
    importlib = None
    import imp

import io, sys
from distutils.version import StrictVersion
_SIX_MIN_VERSION = StrictVersion('1.8.0')
_SIX_SEARCH_PATH = ['vispy.ext._bundled.six', 'six']

def _find_module(name, path=None):
    """
    Alternative to `imp.find_module` that can also search in subpackages.
    """
    parts = name.split('.')
    for part in parts:
        if path is not None:
            path = [
             path]
        fh, path, descr = imp.find_module(part, path)
        if fh is not None and part != parts[(-1)]:
            fh.close()

    return (
     fh, path, descr)


def _import_six(search_path=_SIX_SEARCH_PATH):
    for mod_name in search_path:
        if importlib is not None:
            try:
                six_mod = importlib.import_module(mod_name)
            except ImportError:
                continue

        else:
            try:
                mod_info = _find_module(mod_name)
            except ImportError:
                continue
            else:
                try:
                    six_mod = imp.load_module(__name__, *mod_info)
                finally:
                    if mod_info[0] is not None:
                        mod_info[0].close()

            try:
                if StrictVersion(six_mod.__version__) >= _SIX_MIN_VERSION:
                    break
            except (AttributeError, ValueError):
                continue

    else:
        raise ImportError("Vispy requires the 'six' module of minimum version {0}; normally this is bundled with the Vispy package so if you get this warning consult the packager of your Vispy distribution.".format(_SIX_MIN_VERSION))

    this_module = sys.modules[__name__]
    if not hasattr(this_module, '_importer'):
        for name, value in six_mod.__dict__.items():
            if name.startswith('__'):
                pass
            else:
                this_module.__dict__[name] = value

        importer = six_mod._importer
        known_modules = list(importer.known_modules.items())
        for name, mod in known_modules:
            this_name = __name__ + name[len(mod_name):]
            importer.known_modules[this_name] = mod

        this_module.__path__ = []
        this_module.__package__ = __name__
        if this_module.__dict__.get('__spec__') is not None:
            this_module.__spec__.submodule_search_locations = []


_import_six()
if PY3:
    file_types = (
     io.TextIOWrapper, io.BufferedRandom)
else:
    file_types = (
     file, io.TextIOWrapper, io.BufferedRandom)