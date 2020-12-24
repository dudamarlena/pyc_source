# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/packet/schema.py
# Compiled at: 2013-04-19 10:33:23
from zope.interface import implements
from zope.schema import Object, List
from ztfy.sendit.packet.interfaces import IDocumentField, IDocumentsListField, IDocumentInfo

class DocumentField(Object):
    """Document field"""
    implements(IDocumentField)

    def __init__(self, schema=None, **kw):
        super(DocumentField, self).__init__(schema=IDocumentInfo, **kw)


class DocumentsListField(List):
    """Media documents schema field"""
    implements(IDocumentsListField)

    def __init__(self, value_type=None, unique=False, **kw):
        super(DocumentsListField, self).__init__(value_type=DocumentField(), **kw)