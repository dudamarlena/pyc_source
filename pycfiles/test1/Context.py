# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPath\Context.py
# Compiled at: 2006-12-26 13:39:47
"""
The context of an XPath expression

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from types import ModuleType
import CoreFunctions, BuiltInExtFunctions
from Ft.Xml import XML_NAMESPACE
__all__ = [
 'Context']

class Context:
    __module__ = __name__
    functions = CoreFunctions.CoreFunctions.copy()
    functions.update(BuiltInExtFunctions.ExtFunctions)
    currentInstruction = None

    def __init__(self, node, position=1, size=1, varBindings=None, processorNss=None, extModuleList=None, extFunctionMap=None):
        self.node = node
        self.position = position
        self.size = size
        self.varBindings = varBindings or {}
        self.processorNss = processorNss or {}
        self.processorNss.update({'xml': XML_NAMESPACE})
        functions = self.functions.copy()
        if extModuleList:
            for module in extModuleList:
                if module:
                    if not isinstance(module, ModuleType):
                        module = __import__(module, {}, {}, ['ExtFunctions'])
                    if hasattr(module, 'ExtFunctions'):
                        functions.update(module.ExtFunctions)

        if extFunctionMap:
            functions.update(extFunctionMap)
        self.functions = functions
        return

    def __repr__(self):
        return '<Context at 0x%x: Node=%s, Postion=%d, Size=%d>' % (id(self), self.node, self.position, self.size)

    def addFunction(self, expandedName, function):
        if not callable(function):
            raise TypeError('function must be a callable object')
        self.functions[expandedName] = function
        return

    def copy(self):
        return (
         self.node, self.position, self.size)

    def set(self, state):
        (self.node, self.position, self.size) = state
        return

    def clone(self):
        newobj = self.__class__(self, self.node, self.position, self.size)
        newobj.varBindings = self.varBindings.copy()
        newobj.processorNss = self.processorNss.copy()
        newobj.functions = self.functions
        return newobj