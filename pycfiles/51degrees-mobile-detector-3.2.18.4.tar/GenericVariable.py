# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\GenericVariable.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nBase implementation of XSLT variable assigning elements\n\nCopyright 2002 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import warnings
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import ContentInfo, AttributeInfo
from Ft.Xml.XPath import FT_EXT_NAMESPACE
from Ft.Xml.Xslt.StylesheetTree import XsltNode

class GenericVariableElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Template
    legalAttrs = {'name': AttributeInfo.QName(required=1), 'select': AttributeInfo.Expression(), 'f:node-set': AttributeInfo.YesNoAvt(default='no')}
    doesSetup = True

    def setup(self):
        if (
         FT_EXT_NAMESPACE, 'node-set') in self.attributes:
            warnings.warn('You are using the deprecated f:node-set attribute on xsl:variable or xsl:param.  Please switch to using exslt:node-set', DeprecationWarning, 2)
        if self._select and self.children:
            raise XsltException(Error.VAR_WITH_CONTENT_AND_SELECT, self._name)
        binding_save = self.parent.children[0]
        if not isinstance(binding_save, PushVariablesNode):
            parent = self.parent
            binding_save = PushVariablesNode(parent.root, parent.baseUri)
            parent.insertChild(0, binding_save)
            parent.root.primeInstructions.append(binding_save)
        return

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        if self._select:
            result = self._select.evaluate(context)
        elif self.children:
            processor.pushResultTree(self.baseUri)
            for child in self.children:
                child.instantiate(context, processor)

            result = processor.popResult()
            if self.attributes.get((FT_EXT_NAMESPACE, 'node-set')) == 'yes' and hasattr(result, 'childNodes'):
                result = [result]
        else:
            result = ''
        context.varBindings[self._name] = result
        return


class PushVariablesNode(XsltNode):
    __module__ = __name__

    def __init__(self, root, baseUri):
        self.root = root
        self.baseUri = baseUri
        self.savedVariables = []
        self.popNode = PopVariablesNode(self.savedVariables)
        self._is_primed = False
        return

    def prime(self, processor, context):
        if not self._is_primed:
            self.parent.children.append(self.popNode)
            self._is_primed = True
        return

    def instantiate(self, context, processor):
        self.savedVariables.append(context.varBindings)
        context.varBindings = context.varBindings.copy()
        return

    def isPseudoNode(self):
        return True


class PopVariablesNode(XsltNode):
    __module__ = __name__

    def __init__(self, savedVariables):
        self.savedVariables = savedVariables
        return

    def instantiate(self, context, processor):
        context.varBindings = self.savedVariables.pop()
        return

    def isPseudoNode(self):
        return True