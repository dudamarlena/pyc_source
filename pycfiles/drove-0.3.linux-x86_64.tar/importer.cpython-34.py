# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/util/importer.py
# Compiled at: 2015-02-18 10:54:52
# Size of source mod 2**32: 1127 bytes
"""This module contains classes and methods to import dynamically modules
from specified paths."""
import sys, importlib
from . import temp

def load(module, attr_name=None, anchor=__package__, path=[]):
    """Load a module or an attribute from the specific module.

    >>> load("sys")
    >>> load("sys.environ")
    >>> load(".importer")

    :type module: str
    :param module: The module name to load

    :type attr_name: str
    :param attr_name: The name of the attribute of the module to load (if
        any). If not present, returns the module itself.

    :type anchor: str
    :param anchor: The anchor module to resolve relative module paths. By
        default uses ``__package__``.

    :type path: list
    :param path: a list with paths to search the module
    """
    path = path or sys.path
    with temp.variables({'sys.path': path}):
        mod = importlib.import_module(module, anchor)
        if attr_name:
            return getattr(mod, '%s' % (attr_name,))
        else:
            return mod