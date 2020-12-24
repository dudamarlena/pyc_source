# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/aop.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 28, 2011\n\n@package: ally base\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the AOP (aspect oriented programming) support.\n'
from ..support.util_sys import searchModules, packageModules, isPackage
from ._impl._aop import AOPModules
from .error import AOPError
from inspect import ismodule

def modulesIn(*paths):
    """
    Provides all the modules that are found in the provided package paths.
    
    @param paths: arguments[string|module]
        The package paths to load modules from.
    @return: AOPModules
        The found modules.
    """
    modules = {}
    for path in paths:
        if isinstance(path, str):
            for modulePath in searchModules(path):
                modules[modulePath] = modulePath

        elif ismodule(path):
            if not isPackage(path):
                raise AOPError('The provided module %r is not a package' % path)
            for modulePath in packageModules(path):
                modules[modulePath] = modulePath

        else:
            raise AOPError('Cannot use path %s' % path)

    return AOPModules(modules)


def classesIn(*paths):
    """
    Provides all the classes that are found in the provided pattern paths.
    
    @param paths: arguments[string|module]
        The pattern paths to load classes from.
    @return: AOPClasses
        The found classes.
    """
    modules, filter = {}, []
    for path in paths:
        if isinstance(path, str):
            k = path.rfind('.')
            if k >= 0:
                for modulePath in searchModules(path[:k]):
                    modules[modulePath] = modulePath

            filter.append(path)
        elif ismodule(path):
            modules[path.__name__] = path.__name__
            filter.append('%s.**' % path.__name__)
        else:
            raise AOPError('Cannot use path %s' % path)

    return AOPModules(modules).classes().filter(*filter)