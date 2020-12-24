# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/tools/kssinline.py
# Compiled at: 2008-10-02 13:12:27
__author__ = 'Hedley Roos <hedley@upfrontsystems.co.za>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from collective.kssinline.config import *
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
schema = Schema((LinesField(name='editableTypes', widget=MultiSelectionWidget(label='Editable Types', size=20, label_msgid='kssinline_label_editableTypes', i18n_domain='collective.kssinline'), multiValued=1, vocabulary='editableTypesVocabulary', default_method='defaultEditableTypes'),))
KssInlineTool_schema = BaseSchema.copy() + schema.copy()

class KssInlineTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(interfaces.IKssInlineTool)
    meta_type = 'KssInlineTool'
    _at_rename_after_creation = True
    schema = KssInlineTool_schema

    def __init__(self, id=None):
        BaseContent.__init__(self, 'portal_kssinline')
        self.setTitle('')

    def at_post_edit_script(self):
        self.unindexObject()

    def editableTypesVocabulary(self):
        tool = getToolByName(self, 'portal_types')
        return tool.objectIds()

    def defaultEditableTypes(self):
        return [ t for t in self.editableTypesVocabulary() if t not in ('File', 'Image') ]

    def Title(self):
        return 'KssInline Tool'


registerType(KssInlineTool, PROJECTNAME)