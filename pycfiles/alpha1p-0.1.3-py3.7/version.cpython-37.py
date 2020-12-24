# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/alpha1p/version.py
# Compiled at: 2020-04-14 13:47:26
# Size of source mod 2**32: 1148 bytes
"""Version info"""
import sys, importlib
short_version = '0.1'
version = '0.1.3'

def __get_mod_version(modname):
    try:
        if modname in sys.modules:
            mod = sys.modules[modname]
        else:
            mod = importlib.import_module(modname)
        try:
            return mod.__version__
        except AttributeError:
            return 'installed, no version number available'

    except ImportError:
        return


def show_versions():
    """Return the version information for all librosa dependencies."""
    core_deps = [
     'usb',
     'numpy',
     'pandas',
     'serial']
    extra_deps = [
     'math',
     'numba',
     'pkg_resources']
    print('INSTALLED VERSIONS')
    print('------------------')
    print('python: {}\n'.format(sys.version))
    print('alpha1p: {}\n'.format(version))
    for dep in core_deps:
        print('{}: {}'.format(dep, __get_mod_version(dep)))

    print('')
    for dep in extra_deps:
        print('{}: {}'.format(dep, __get_mod_version(dep)))