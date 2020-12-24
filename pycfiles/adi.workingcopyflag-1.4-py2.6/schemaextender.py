# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/workingcopyflag/schemaextender.py
# Compiled at: 2012-11-19 05:25:18
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.markerfield.field import InterfaceMarkerField
from Products.ATContentTypes.interface import IATContentType
from Products.Archetypes.atapi import BooleanWidget
from adi.workingcopyflag.interfaces import IWorkingcopyFlaggableObject
_ = MessageFactory('adi.workingcopyflag')

class ContentTypeExtender(object):
    """Adapter that adds custom metadata."""
    adapts(IATContentType)
    implements(ISchemaExtender)
    _fields = [
     InterfaceMarkerField('workingcopyflag', schemata='settings', interfaces=(
      IWorkingcopyFlaggableObject,), languageIndependent=True, visible={'edit': 'hidden', 'view': 'hidden'}, widget=BooleanWidget(label=_('label_workingcopyflag_title', default='Has a workingcopy'), description=_('help_workingcopyflag', default='If this field is marked, this item does have a working copy.')))]

    def __init__(self, contentType):
        pass

    def getFields(self):
        return self._fields