# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/pkg.py
# Compiled at: 2014-03-14 23:17:29
# Size of source mod 2**32: 536 bytes
__doc__ = '\nPackages related utility functions\n'
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