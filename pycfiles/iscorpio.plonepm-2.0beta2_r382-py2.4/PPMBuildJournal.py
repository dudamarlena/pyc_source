# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMBuildJournal.py
# Compiled at: 2009-09-03 11:41:06
"""PPMBuildJournal Product for Plone to record build
journal."""
__author__ = 'iScorpio'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import *
PPMBuildJournalSchema = ATCTContent.schema.copy() + Schema((TextField('buildJournalBody', searchable=True, required=True, allowable_content_types=('text/plain',
                                                                                       'text/structured',
                                                                                       'text/html'), default_output_type='text/x-html-safe', widget=RichWidget(label='Build Journal Body', rows=28)),))
PPMBuildJournalSchema['subject'].schemata = 'default'
PPMBuildJournalSchema['subject'].required = True
PPMBuildJournalSchema['subject'].widget.label = 'Projects'
PPMBuildJournalSchema['subject'].widget.size = 6
PPMBuildJournalSchema.moveField('subject', after='description')
PPMBuildJournalSchema['relatedItems'].widget.visible = True
PPMBuildJournalSchema.moveField('relatedItems', pos='bottom')

class PPMBuildJournal(ATCTContent, HistoryAwareMixin):
    __module__ = __name__
    schema = PPMBuildJournalSchema
    meta_type = 'BuildJournal'
    archetype_name = 'BuildJournal'
    portal_type = 'BuildJournal'
    content_icon = 'document_icon.gif'
    _at_rename_after_creation = True
    default_view = 'base_view'
    global_allow = True
    security = ClassSecurityInfo()


registerType(PPMBuildJournal, PROJECTNAME)