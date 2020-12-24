# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\LiteralElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of XSLT literal result elements\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml.XPath import RuntimeException as XPathRuntimeException
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error

class LiteralElement(XsltElement):
    __module__ = __name__
    _use_attribute_sets = []

    def fixupAliases(self, namespaceAliases):
        if self._output_namespace in namespaceAliases:
            alias_info = namespaceAliases[self._output_namespace]
            (self._output_namespace, prefix) = alias_info
            if prefix:
                self.nodeName = (':').join([prefix, self.expandedName[1]])
            else:
                self.nodeName = self.expandedName[1]
        pos = 0
        for (qname, namespace, value) in self._output_attrs:
            if namespace and namespace in namespaceAliases:
                (namespace, prefix) = namespaceAliases[namespace]
                local = qname.split(':')[(-1)]
                if prefix:
                    qname = (':').join([prefix, local])
                else:
                    qname = local
                self._output_attrs[pos] = (
                 qname, namespace, value)
            pos += 1

        for (prefix, namespace) in self._output_nss.items():
            if namespace in namespaceAliases:
                del self._output_nss[prefix]
                (namespace, prefix) = namespaceAliases[namespace]
                self._output_nss[prefix] = namespace

        return

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        processor.writers[(-1)].startElement(self.nodeName, self._output_namespace, self._output_nss)
        for (qname, namespace, value) in self._output_attrs:
            try:
                value = value.evaluate(context)
            except XPathRuntimeException, e:
                import MessageSource
                e.message = MessageSource.EXPRESSION_POSITION_INFO % (self.baseUri, self.lineNumber, self.columnNumber, value.source, str(e))
                raise
            except XsltRuntimeException, e:
                import MessageSource
                e.message = MessageSource.XSLT_EXPRESSION_POSITION_INFO % (str(e), value.source)
                raise
            except Exception, e:
                import MessageSource, cStringIO, traceback
                tb = cStringIO.StringIO()
                tb.write('Lower-level traceback:\n')
                traceback.print_exc(1000, tb)
                raise RuntimeError(MessageSource.EXPRESSION_POSITION_INFO % (self.baseUri, self.lineNumber, self.columnNumber, value.source, tb.getvalue()))

            processor.writers[(-1)].attribute(qname, value, namespace)

        for attr_set_name in self._use_attribute_sets:
            try:
                attr_set = processor.attributeSets[attr_set_name]
            except KeyError:
                raise XsltRuntimeException(Error.UNDEFINED_ATTRIBUTE_SET, self, attr_set_name)

            attr_set.instantiate(context, processor)

        for child in self.children:
            child.instantiate(context, processor)

        processor.writers[(-1)].endElement(self.nodeName, self._output_namespace)
        return