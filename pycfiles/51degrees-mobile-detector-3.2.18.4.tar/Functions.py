# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Exslt\Functions.py
# Compiled at: 2005-12-10 14:51:55
__doc__ = '\nEXSLT 2.0 - Functions (http://www.exslt.org/func/index.html)\nWWW: http://4suite.org/XSLT        e-mail: support@4suite.org\n\nCopyright (c) 2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml import XPath
from Ft.Xml.Xslt import XSL_NAMESPACE, XsltElement
from Ft.Xml.Xslt import XsltRuntimeException
from Ft.Xml.Xslt import ContentInfo, AttributeInfo
from Ft.Xml.Xslt.Exslt.MessageSource import Error as ExsltError
from Ft.Xml.Xslt.XPathExtensions import RtfExpr
EXSL_FUNCTIONS_NS = 'http://exslt.org/functions'

class FunctionElement(XsltElement):
    __module__ = __name__
    content = ContentInfo.Seq(ContentInfo.Rep(ContentInfo.QName(XSL_NAMESPACE, 'xsl:param')), ContentInfo.Template)
    legalAttrs = {'name': AttributeInfo.QNameButNotNCName(required=1)}
    doesPrime = True

    def prime(self, processor, context):
        context.addFunction(self._name, self)
        return

    def __call__(self, context, *args):
        processor = context.processor
        ctx_state = context.copy()
        ctx_namespaces = context.processorNss
        ctx_instruction = context.currentInstruction
        context.processorNss = self.namespaces
        context.currentInstruction = self
        counter = 0
        self.result = ''
        for child in self.children:
            if child.expandedName == (XSL_NAMESPACE, 'param'):
                if counter < len(args):
                    context.varBindings[child._name] = args[counter]
                else:
                    child.instantiate(context, processor)
                counter = counter + 1
            else:
                child.instantiate(context, processor)

        context.currentInstruction = ctx_instruction
        context.processorNss = ctx_namespaces
        context.set(ctx_state)
        return self.result


class ResultElement(XsltElement):
    """
    When an func:result element is instantiated, during the
    instantiation of a func:function element, the function returns
    with its value.
    """
    __module__ = __name__
    content = ContentInfo.Template
    legalAttrs = {'select': AttributeInfo.Expression()}
    doesSetup = doesPrime = True

    def setup(self):
        if not self._select:
            self._select = RtfExpr(self.children)
        return

    def prime(self, processor, context):
        self._function = None
        current = self.parent
        while current:
            if current.expandedName == (EXSL_FUNCTIONS_NS, 'function'):
                self._function = current
                break
            current = current.parent

        if not self._function:
            raise XsltRuntimeException(ExsltError.RESULT_NOT_IN_FUNCTION, self)
        if not self.isLastChild():
            siblings = self.parent.children
            for node in siblings[siblings.index(self) + 1:]:
                if node.expandedName != (XSL_NAMESPACE, 'fallback'):
                    raise XsltRuntimeException(ExsltError.ILLEGAL_RESULT_SIBLINGS, self)

        return
        return

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        self._function.result = self._select.evaluate(context)
        return


class ScriptElement(XsltElement):
    """
    NOT YET IMPLEMENTED

    The top-level func:script element provides an implementation of
    extension functions in a particular namespace.
    """
    __module__ = __name__


ExtNamespaces = {EXSL_FUNCTIONS_NS: 'func'}
ExtFunctions = {}
ExtElements = {(EXSL_FUNCTIONS_NS, 'function'): FunctionElement, (EXSL_FUNCTIONS_NS, 'result'): ResultElement}