# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPointer\XPtrContext.py
# Compiled at: 2002-07-16 18:37:23
from Ft.Xml.XPath import Context
import XPtrFunctions

class XPtrContext(Context.Context):
    __module__ = __name__

    def __init__(self, node, position, size, originalContext, processorNss=None, extModuleList=None, extFunctionMap=None):
        extFunctionMap = extFunctionMap or {}
        extFunctionMap.update(XPtrFunctions.CoreFunctions)
        Context.Context.__init__(self, node, position, size, {}, processorNss, extModuleList=extModuleList, extFunctionMap=extFunctionMap)
        self.originalContext = originalContext

    def __repr__(self):
        return '<XPtrContext at %x: Node=%s, Pos="%d", Size="%d", Origin=%s>' % (id(self), repr(self.node), self.position, self.size, repr(self.originalContext))