# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/pkg.py
# Compiled at: 2014-03-14 23:17:29
# Size of source mod 2**32: 536 bytes
"""
Packages related utility functions
"""
import pkgutil

def get_submodules(package):
    """
    Returns all sub-modules of a package also indicating if the module is also a package
    Return a list with each item being a dictionary with keys name (String) and is_package (Boolean)
    """
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        ret.append({'name': modname, 'is_package': ispkg})

    return ret