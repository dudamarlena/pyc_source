# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ApplyTemplatesElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of xsl:apply-templates instruction\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XSL_NAMESPACE, XsltRuntimeException, Error
from Ft.Xml.Xslt import CategoryTypes, AttributeInfo, ContentInfo
from Ft.Xml.Xslt.XPathExtensions import SortedExpression

class ApplyTemplatesElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Rep(ContentInfo.Alt(ContentInfo.QName(XSL_NAMESPACE, 'xsl:sort'), ContentInfo.QName(XSL_NAMESPACE, 'xsl:with-param')))
    legalAttrs = {'select': AttributeInfo.Expression(), 'mode': AttributeInfo.QName()}
    doesSetup = 1

    def setup(self):
        sort_keys = []
        self._params = []
        for child in self.children:
            name = child.expandedName[1]
            if name == 'sort':
                sort_keys.append(child)
            elif name == 'with-param':
                self._params.append((child, child._name, child._select))

        if sort_keys:
            self._select = SortedExpression(self._select, sort_keys)
        return

    def _instantiate_mode(self, context):
        return self._mode

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        with_params = {}
        for (param, name, expr) in self._params:
            context.processorNss = param.namespaces
            context.currentInstruction = param
            with_params[name] = expr.evaluate(context)

        if self._select:
            node_set = self._select.evaluate(context)
            if not isinstance(node_set, list):
                raise XsltRuntimeException(Error.ILLEGAL_APPLYTEMPLATE_NODESET, self)
        else:
            node_set = context.node.childNodes
        state = context.copy()
        mode = context.mode
        context.mode = self._instantiate_mode(context)
        pos = 1
        size = len(node_set)
        for node in node_set:
            (context.node, context.position, context.size) = (
             node, pos, size)
            processor.applyTemplates(context, with_params)
            pos += 1

        context.mode = mode
        context.set(state)
        return