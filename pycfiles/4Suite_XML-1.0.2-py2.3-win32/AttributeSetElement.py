# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\AttributeSetElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec attribute-set stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
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