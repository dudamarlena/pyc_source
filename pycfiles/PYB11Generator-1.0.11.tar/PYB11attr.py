# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11attr.py
# Compiled at: 2019-03-04 00:14:46
from PYB11utils import *
import sys, inspect

def PYB11generateModuleAttrs(modobj, ss):
    stuff = [ x for x in dir(modobj) if isinstance(eval('modobj.%s' % x), PYB11attr) ]
    if stuff:
        ss('\n  // module attributes\n')
        for pyname in stuff:
            inst = eval('modobj.%s' % pyname)
            inst(pyname, ss)


class PYB11attr:

    def __init__(self, value=None, pyname=None):
        self.value = value
        self.pyname = pyname

    def __call__(self, pyname, ss):
        if self.pyname:
            self.__name__ = self.pyname
        else:
            self.__name__ = pyname
        attrattrs = PYB11attrs(self)
        if self.value:
            attrattrs['cppname'] = self.value
        else:
            attrattrs['cppname'] = pyname
        ss('  m.attr("%(pyname)s") = %(cppname)s;\n' % attrattrs)