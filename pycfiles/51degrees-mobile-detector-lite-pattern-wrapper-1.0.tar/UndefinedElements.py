# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\UndefinedElements.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nNode classes for the stylesheet tree\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml.Xslt import XSL_NAMESPACE, XsltElement
from Ft.Xml.Xslt import XsltRuntimeException, Error
from Ft.Xml.Xslt import CategoryTypes, ContentInfo

class _UndefinedElement(XsltElement):
    __module__ = __name__

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        fallback = False
        for child in self.children:
            if child.expandedName == (XSL_NAMESPACE, 'fallback'):
                fallback = True
                for fallback_child in child.children:
                    fallback_child.instantiate(context, processor)

        if not fallback:
            raise self._getError()
        return

    def _getError(self):
        raise NotImplemented


class UndefinedXsltElement(_UndefinedElement):
    __module__ = __name__
    legalAttrs = {}

    def _getError(self):
        return XsltRuntimeException(Error.FWD_COMPAT_WITHOUT_FALLBACK, self, self.expandedName[1])


class UndefinedExtensionElement(_UndefinedElement):
    __module__ = __name__
    legalAttrs = None

    def _getError(self):
        return XsltRuntimeException(Error.UNKNOWN_EXTENSION_ELEMENT, self, *self.expandedName)