# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/paths/Paths.py
# Compiled at: 2013-12-08 21:45:16
from .SingletonByName import SingletonByName

class Paths(SingletonByName):

    def __init__(self, name, root=None, includes=None, clibs=None, modules=None, description=None, origin=None):
        self.name = name
        self._defaults()
        if root:
            self.root = root
        if includes:
            self.includes = includes
        if clibs:
            self.clibs = clibs
        if modules:
            self.modules = modules
        if description:
            self.description = description
        if origin:
            self.origin = origin
        import traceback
        stack = traceback.extract_stack()
        source, line, function, text = stack[(-2)]
        import os
        visitor = source.split(os.path.sep)[(-1)].split('.')[0]
        try:
            self.visitors.append(visitor)
        except AttributeError:
            self.visitors = [
             visitor]

    def _defaults(self):
        if self.__dict__.get('description') is None:
            self.description = ''
        if self.__dict__.get('origin') is None:
            self.origin = ''
        if self.__dict__.get('root') is None:
            self.root = ''
        if self.__dict__.get('includes') is None:
            self.includes = []
        if self.__dict__.get('clibs') is None:
            self.clibs = []
        if self.__dict__.get('modules') is None:
            self.modules = []
        return

    def __str__(self):
        s = 'Paths for %r, the %r, are obtained by %r. \n' % (self.name, self.description, self.origin)
        s += '  root     = %s\n' % self.root
        s += '  includes = %s\n' % self.includes
        s += '  clibs    = %s\n' % self.clibs
        s += '  modules  = %s\n' % self.modules
        return s