# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/__init__.py
# Compiled at: 2018-01-12 14:07:43
# Size of source mod 2**32: 1068 bytes
import imp, os, sys, warnings

def _import_module(name, relpath):
    """Imports a module from a path relative to this one's."""
    try:
        fp, pathname, description = imp.find_module(name)
        return imp.load_module(name, fp, pathname, description)
    except ImportError:
        pass

    try:
        path = os.path.join(os.path.dirname(__file__), relpath)
        fp, filename, description = imp.find_module(name, [path])
        return imp.load_module(name, fp, filename, description)
    except IOError:
        warnings.warn('Marvin cannot import {0}'.format(name), ImportWarning)
        return


sqlalchemy_boolean_search = _import_module('sqlalchemy_boolean_search', 'sqlalchemy-boolean-search/')
wtforms_alchemy = _import_module('wtforms_alchemy', 'wtforms-alchemy/')
brain = _import_module('brain', 'marvin_brain/python')