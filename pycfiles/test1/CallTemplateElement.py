# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\CallTemplateElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec call-template stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
from xml.dom import Node
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, AttributeInfo, ContentInfo

class CallTemplateElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Rep(ContentInfo.QName(XSL_NAMESPACE, 'xsl:with-param'))
    legalAttrs = {'name': AttributeInfo.QName(required=1)}
    doesSetup = doesPrime = 1

    def setup(self):
        self._tail_recursive = 0
        self._called_template = None
        self._params = map(lambda with_param: (with_param, with_param._name, with_param._select), self.children)
        return
        return

    def prime(self, processor, context):
        self._called_template = processor._namedTemplates.get(self._name)
        if not self._called_template:
            return
        current = self.parent
        while current is not processor.stylesheet:
            if current is self._called_template:
                if self.isLastChild():
                    use_tail = 1
                    node = self.parent
                    while node is not current:
                        if not (node.isLastChild() and node.expandedName[0] == XSL_NAMESPACE and node.expandedName[1] in ['choose', 'if', 'otherwise', 'when']):
                            use_tail = 0
                            break
                        node = node.parent

                    self._tail_recursive = use_tail
                break
            current = current.parent

        return

    def instantiate(self, context, processor):
        if not self._called_template:
            self.prime(processor, context)
            self._called_template = processor._namedTemplates.get(self._name)
            if not self._called_template:
                raise XsltRuntimeException(Error.NAMED_TEMPLATE_NOT_FOUND, self, self._name)
            self._called_template.prime(processor, context)
        params = {}
        for (param, name, expr) in self._params:
            context.processorNss = param.namespaces
            context.currentInstruction = param
            params[name] = expr.evaluate(context)

        if self._tail_recursive:
            context.recursiveParams = params
        else:
            context.currentNode = context.node
            self._called_template.instantiate(context, processor, params)
        return