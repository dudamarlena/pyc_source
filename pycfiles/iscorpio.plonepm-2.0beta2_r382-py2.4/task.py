# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/task.py
# Compiled at: 2009-09-03 11:41:06
"""XPointTask defines the task for a XPointStory
journal."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import IntDisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import PROJECTNAME
XPointTaskSchema = ATFolderSchema.copy() + Schema((TextField('xptask_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Task description', rows=25)), DateTimeField('xptask_completion_date', index='DateIndex:schema', searchable=False, required=True, widget=CalendarWidget(label='90% Completion Deadline', description='Specify the date when this task should be completed at less 90%', starting_year=2007, show_hm=False)), IntegerField('xptask_progress_percent', index='FieldIndex:schema', searchable=False, required=True, default=0, vocabulary=IntDisplayList([ (i, i) for i in range(0, 101) ]), widget=SelectionWidget(label='Progress Status', descrpiton='Progress status in percentage 0% - 100%', format='select')), IntegerField('xptask_estimated_hours', index='FieldIndex:schema', searchable=False, required=False, widget=IntegerWidget(label='Estimated Hours', descrpiton='Put here the estimated hours for this task')), IntegerField('xptask_used_hours', index='FieldIndex:schema', searchable=False, required=False, widget=IntegerWidget(label='Actual Used Hours', descrpiton='Put here the actual used hours for this task')), LinesField('xptask_owners', index='KeywordIndex:schema', searchable=False, required=False, vocabulary='vocabulary_developers', widget=InAndOutWidget(label='Task Owner(s)', descrpiton='Please select owners for this task'))))
finalizeATCTSchema(XPointTaskSchema)
XPointTaskSchema['description'].widget.visible = False

class XPointTask(ATFolder):
    """The ATConentType class for a XPointTask.
    """
    __module__ = __name__
    schema = XPointTaskSchema
    meta_type = 'XPointTask'
    portal_type = 'XPointTask'
    archetype_name = 'XP Task'
    _at_rename_after_creation = True
    __implements__ = (
     ATFolder.__implements__, IATFolder)
    security = ClassSecurityInfo()

    def vocabulary_developers(self):
        """ Return a list of tuple (user_id, fullname, email) for all
        the members of the portal.
        """
        members = []
        portalMembers = getToolByName(self, 'portal_membership')
        developers = self.getProjectDevelopers()
        for memberId in developers:
            members.append((memberId, portalMembers.getMemberById(memberId).getProperty('fullname', None)))

        return DisplayList(members)

    security.declarePublic('getTaskMemos')

    def getTaskMemos(self):
        """ returns all memos about this task.
        """
        return self.contentValues(filter={'portal_type': ['XPointMemo']})

    security.declarePublic('getTaskIssues')

    def getTaskIssues(self):
        """ returns all issues of this task.
        """
        return self.contentValues(filter={'portal_type': ['XPointIssue']})

    security.declarePublic('getTaskProposals')

    def getTaskProposals(self):
        """ retruns all proposals for this task.
        """
        return self.contentValues(filter={'portal_type': ['XPointProposal']})

    security.declarePublic('getTaskMemosIssuesProposals')

    def getTaskMemosIssuesProposals(self):
        """ returns all memos, issues, proposals for this task.
        """
        return self.contentValues(filter={'portal_type': ['XPointMemo', 'XPointIssue', 'XPointProposal']})


registerType(XPointTask, PROJECTNAME)