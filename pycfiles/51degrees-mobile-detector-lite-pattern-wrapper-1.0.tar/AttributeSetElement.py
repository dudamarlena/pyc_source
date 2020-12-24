# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\AttributeSetElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec attribute-set stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, AttributeInfo, ContentInfo

class AttributeSetElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Rep(ContentInfo.QName(XSL_NAMESPACE, 'xsl:attribute'))
    legalAttrs = {'name': AttributeInfo.QName(required=1), 'use-attribute-sets': AttributeInfo.QNames()}
    doesPrime = 1

    def prime(self, processor, context):
        processor.attributeSets[self._name] = self
        return

    def instantiate(self, context, processor, used=None):
        if used is None:
            used = []
        if self in used:
            raise XsltRuntimeException(Error.CIRCULAR_ATTRIBUTE_SET, self, self._name)
        else:
            used.append(self)
        old_vars = context.varBindings
        context.varBindings = processor.stylesheet.getGlobalVariables()
        for attr_set_name in self._use_attribute_sets:
            try:
                attr_set = processor.attributeSets[attr_set_name]
            except KeyError:
                raise XsltRuntimeException(Error.UNDEFINED_ATTRIBUTE_SET, self, attr_set_name)

            attr_set.instantiate(context, processor, used)

        for child in self.children:
            child.instantiate(context, processor)

        context.varBindings = old_vars
        used.remove(self)
        return
        return