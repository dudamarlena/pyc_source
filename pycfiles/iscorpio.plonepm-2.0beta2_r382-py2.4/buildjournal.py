# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/buildjournal.py
# Compiled at: 2009-09-03 11:41:06
"""XPointBuildJournal Product for Plone to record build
journal."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from iscorpio.plonepm.content.xpointdoc import XPointDocument
from iscorpio.plonepm.config import PROJECTNAME
XPointBuildJournalSchema = XPointDocument.schema.copy()
XPointBuildJournalSchema['subject'].schemata = 'default'
XPointBuildJournalSchema['subject'].required = True
XPointBuildJournalSchema['subject'].widget.label = 'Projects'
XPointBuildJournalSchema['subject'].widget.description = 'Select projects for this build journal, holding CTRL key to select more than one project'
XPointBuildJournalSchema['subject'].widget.size = 6
XPointBuildJournalSchema.moveField('subject', after='description')

class XPointBuildJournal(XPointDocument):
    __module__ = __name__
    schema = XPointBuildJournalSchema
    meta_type = 'XPointBuildJournal'
    portal_type = 'XPointBuildJournal'
    archetype_name = 'Build Journal'
    security = ClassSecurityInfo()


registerType(XPointBuildJournal, PROJECTNAME)