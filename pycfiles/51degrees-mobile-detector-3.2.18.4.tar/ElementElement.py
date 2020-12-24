# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ElementElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of xsl:element element\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo

class ElementElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {'name': AttributeInfo.RawQNameAvt(required=1), 'namespace': AttributeInfo.UriReferenceAvt(isNsName=1), 'use-attribute-sets': AttributeInfo.QNames()}

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        (prefix, local) = self._name.evaluate(context)
        if prefix is not None:
            name = prefix + ':' + local
        else:
            name = local
        if not self._namespace:
            if prefix is not None:
                if not self.namespaces.has_key(prefix):
                    raise XsltRuntimeException(Error.UNDEFINED_PREFIX, self, prefix)
                namespace = self.namespaces[prefix]
            else:
                namespace = self.namespaces[None]
        else:
            namespace = self._namespace and self._namespace.evaluate(context) or EMPTY_NAMESPACE
        self.execute(context, processor, name, namespace)
        return
        return

    def execute(self, context, processor, name, namespace):
        processor.writers[(-1)].startElement(name, namespace)
        for attr_set_name in self._use_attribute_sets:
            try:
                attr_set = processor.attributeSets[attr_set_name]
            except KeyError:
                raise XsltRuntimeException(Error.UNDEFINED_ATTRIBUTE_SET, self, attr_set_name)

            attr_set.instantiate(context, processor)

        for child in self.children:
            child.instantiate(context, processor)

        processor.writers[(-1)].endElement(name, namespace)
        return