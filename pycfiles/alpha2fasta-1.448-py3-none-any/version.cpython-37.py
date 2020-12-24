# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/alpha1p/version.py
# Compiled at: 2020-04-14 13:47:26
# Size of source mod 2**32: 1148 bytes
__doc__ = 'Version info'
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