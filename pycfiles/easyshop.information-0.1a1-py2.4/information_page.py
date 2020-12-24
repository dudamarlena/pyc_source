# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/content/information_page.py
# Compiled at: 2008-09-03 11:14:54
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.document import ATDocumentSchema
from easyshop.core.config import *
from easyshop.core.interfaces import IInformationPage
schema = ATFolderSchema.copy() + ATDocumentSchema.copy() + Schema((FileField(name='file', widget=FileWidget(label='File', label_msgid='schema_file_label', description='Upload of the original document.', description_msgid='schema_file_description', i18n_domain='EasyShop')),))
finalizeATCTSchema(schema, moveDiscussion=False)

class InformationPage(ATFolder):
    """
    """
    __module__ = __name__
    implements(IInformationPage)
    _at_rename_after_creation = True
    schema = schema


registerType(InformationPage, PROJECTNAME)