# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/keywordwidgetreplacer/linesfield_adapter.py
# Compiled at: 2008-08-22 16:25:09
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.ATContentTypes.interface import IATContentType
from Products.AddRemoveWidget import AddRemoveWidget
from Products.Archetypes import atapi
from zope.interface import implements
from zope.component import adapts

class SchemaModifier(object):
    __module__ = __name__
    implements(ISchemaModifier)
    adapts(IATContentType)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        fields = [ i for i in schema.values() if isinstance(i, atapi.LinesField) if isinstance(i.widget, atapi.KeywordWidget) ]
        for field in fields:
            oldlabel = field.widget.label
            olddesc = field.widget.description
            field.widget = AddRemoveWidget(label=oldlabel, description=olddesc, role_based_add=True)