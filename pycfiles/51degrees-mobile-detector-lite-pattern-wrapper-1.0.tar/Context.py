# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\Context.py
# Compiled at: 2006-12-26 13:39:47
__doc__ = '\nThe context of an XPath expression\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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