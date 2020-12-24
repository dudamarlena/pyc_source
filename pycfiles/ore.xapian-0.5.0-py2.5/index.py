# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/index.py
# Compiled at: 2008-09-11 20:29:58
import xappy
from zope import interface, schema
import interfaces

class DefaultContentIndexer(object):
    interface.implements(interfaces.IIndexer)

    def __init__(self, context):
        self.context = context

    def document(self, connection):
        """
        return a xapian index document from the context.

        we can introspect the connection to discover relevant fields available.
        """
        doc = xappy.UnprocessedDocument()
        for iface in interface.providedBy(self.context):
            for field in schema.getFields(iface).values():
                if not isinstance(field, (schema.Text, schema.ASCII)):
                    continue
                value = field.query(self.context)
                if value is None:
                    value = ''
                if not isinstance(value, (str, unicode)):
                    value = unicode(value)
                doc.fields.append(xappy.Field(field.__name__, value))

        return doc