# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/xpointdoc.py
# Compiled at: 2009-09-03 11:41:06
"""XPointDocument is the super class of PlonePM general
documents, such as memo, buildjounal, proposal, and issue."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.permissions import View
XPointDocumentSchema = ATCTContent.schema.copy() + Schema((TextField('xpproject_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Body Text', rows=22)), StringField('xpproject_document_status', searchable=False, required=False, index='FieldIndex:schema', default='', vocabulary='vocabulary_documentStatus', widget=SelectionWidget(label='Document Status', descrpiton='Set status for this issue.', format='select'))))
finalizeATCTSchema(XPointDocumentSchema)
XPointDocumentSchema['xpproject_document_status'].widget.visible = False
XPointDocumentSchema['relatedItems'].widget.visible = True
XPointDocumentSchema['relatedItems'].widget.description = 'Select related items'
XPointDocumentSchema['relatedItems'].schemata = 'default'
XPointDocumentSchema.moveField('relatedItems', pos='bottom')

class XPointDocument(ATCTContent, HistoryAwareMixin):
    __module__ = __name__
    schema = XPointDocumentSchema
    __implements__ = (
     ATCTContent.__implements__, IATDocument, HistoryAwareMixin.__implements__)
    _at_rename_after_creation = True
    security = ClassSecurityInfo()
    security.declareProtected(View, 'CookedBody')

    def CookedBody(self, stx_level='ignored'):
        """CMF compatibility method
        """
        return self.getXpproject_text()

    def initializeArchetype(self, **kwargs):
        ATCTContent.initializeArchetype(self, **kwargs)

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'), ('close', 'Close')])