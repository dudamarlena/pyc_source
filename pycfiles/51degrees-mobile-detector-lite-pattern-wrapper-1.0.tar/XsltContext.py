# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\XsltContext.py
# Compiled at: 2006-12-26 13:39:47
__doc__ = '\nContext and state information for XSLT processing\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import Exslt, BuiltInExtFunctions
from Ft.Lib.Uri import UriDict
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.XPath import Context, Util, RuntimeException
from Ft.Xml.Xslt import XsltFunctions

class XsltContext(Context.Context):
    __module__ = __name__
    functions = Context.Context.functions.copy()
    functions.update(XsltFunctions.CoreFunctions)
    functions.update(Exslt.ExtFunctions)
    functions.update(BuiltInExtFunctions.ExtFunctions)

    def __init__(self, node, position=1, size=1, currentNode=None, varBindings=None, processorNss=None, stylesheet=None, processor=None, mode=None, extModuleList=None, extFunctionMap=None):
        Context.Context.__init__(self, node, position, size, varBindings, processorNss, extModuleList, extFunctionMap)
        self.currentNode = currentNode
        self.stylesheet = stylesheet
        self.mode = mode
        self.processor = processor
        self.documents = UriDict()
        self.rtfs = []
        self.currentInstruction = None
        self.recursiveParams = None
        return
        return

    def addDocument(self, document, documentUri=None):
        if documentUri:
            self.documents[documentUri] = document
        return

    def splitQName(self, qname):
        if not qname:
            return None
        index = qname.find(':')
        if index != -1:
            split = (
             qname[:index], qname[index + 1:])
        else:
            split = (
             None, qname)
        return split
        return

    def expandQName(self, qname):
        if not qname:
            return None
        (prefix, local) = self.splitQName(qname)
        if prefix:
            try:
                expanded = (
                 self.processorNss[prefix], local)
            except KeyError:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

        else:
            expanded = (
             EMPTY_NAMESPACE, local)
        return expanded
        return

    def setProcessState(self, execNode):
        self.processorNss = execNode.namespaces
        self.currentInstruction = execNode
        return

    def clone(self):
        ctx = XsltContext(self.node, self.position, self.size, self.currentNode, self.varBindings.copy(), self.processorNss, self.stylesheet, self.processor, self.mode)
        ctx.functions = self.functions
        return ctx

    def __repr__(self):
        return '<XsltContext at %x: node %s, position %d, size %d, mode %r>' % (id(self), repr(self.node), self.position, self.size, self.mode)