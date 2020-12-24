# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/importer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2446 bytes
from . import load
from . import fields
from distutils.version import LooseVersion
MINIMUM_VERSIONS = {'serial': '2.7'}
INSTALL_NAMES = {'BiblioPixelAnimations':'BiblioPixelAnimations', 
 'flask':'flask', 
 'noise':'noise', 
 'serial':'pyserial'}

def _validate_typename(typename):
    root_module = typename.split('.')[0]
    min_version = MINIMUM_VERSIONS.get(root_module)
    if not min_version:
        return
    version = __import__(root_module).VERSION
    if LooseVersion(version) < LooseVersion(min_version):
        install_name = INSTALL_NAMES.get(root_module, root_module)
        raise ValueError(VERSION_MESSAGE % (
         root_module, version, min_version, install_name))


def _import(typename, python_path=None, loader=load.code):
    try:
        result = loader(typename, python_path=python_path)
        _validate_typename(typename)
        return result
    except ImportError as e:
        root_module = typename.split('.')[0]
        install_name = INSTALL_NAMES.get(root_module)
        if install_name:
            try:
                __import__(root_module)
            except ImportError:
                msg = MISSING_MESSAGE % (root_module, install_name)
                e.msg = msg + e.msg

        raise


def import_symbol(typename, python_path=None):
    return _import(typename, python_path)


def import_module(typename, python_path=None):
    return _import(typename, python_path, loader=(load.module))


def make_object(*args, typename=None, python_path=None, datatype=None, **kwds):
    """Make an object from a symbol."""
    datatype = datatype or import_symbol(typename, python_path)
    field_types = getattr(datatype, 'FIELD_TYPES', fields.FIELD_TYPES)
    return datatype(*args, **fields.component(kwds, field_types))


VERSION_MESSAGE = "\nYou have version %s of module '%s' but you need version %s.\n\nPlease upgrade at the command line with:\n\n    $ pip install %s --upgrade\n"
MISSING_MESSAGE = "\nYou are missing module '%s'.\n\nPlease install it at the command line with:\n\n    $ pip install %s\n"
SERIAL_IS_INSTALLED_NOT_PYSERIAL_MESSAGE = "\nYou have the module `serial` installed, but you need the package `pyserial`\ninstead.  Sorry, it's not our fault that there are two packages whose names are\nso close!\n\nTo uninstall that module and install the correct one from the command line:\n\n    $ pip uninstall -y serial\n    $ pip install pyserial\n"