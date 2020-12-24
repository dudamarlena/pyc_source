# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ForEachElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec for-each stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo
from Ft.Xml.Xslt.XPathExtensions import SortedExpression
from Ft.Xml.Xslt.SortElement import SortElement

class ForEachElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Seq(ContentInfo.Rep(ContentInfo.QName(XSL_NAMESPACE, 'xsl:sort')), ContentInfo.Template)
    legalAttrs = {'select': AttributeInfo.NodeSetExpression(required=1)}
    doesSetup = 1

    def setup(self):
        sort_keys = filter(lambda x: isinstance(x, SortElement), self.children)
        if sort_keys:
            self._select = SortedExpression(self._select, sort_keys)
        return

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        if self._select:
            node_set = self._select.evaluate(context)
            if type(node_set) != type([]):
                raise XsltRuntimeException(Error.INVALID_FOREACH_SELECT, self)
        else:
            node_set = context.node.childNodes
        state = context.copy()
        pos = 1
        size = len(node_set)
        for node in node_set:
            (context.node, context.position, context.size) = (
             node, pos, size)
            context.currentNode = node
            for child in self.children:
                child.instantiate(context, processor)

            pos += 1

        context.set(state)
        return