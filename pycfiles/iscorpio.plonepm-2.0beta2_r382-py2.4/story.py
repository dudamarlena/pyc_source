# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/story.py
# Compiled at: 2009-09-03 11:41:06
"""XPointStory defines a topic/module/component for a
XPointProject."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import PROJECTNAME
XPointStorySchema = ATFolderSchema.copy() + Schema((TextField('xpstory_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Story body', rows=22)), StringField('xpstory_module', searchable=False, required=True, vocabulary='getProjectModules', default='mosapp', widget=SelectionWidget(label='Module', description='Select the module for this story', format='select')), LinesField('xpstory_releases', searchable=True, required=True, vocabulary='vocabulary_releases', widget=InAndOutWidget(label='Planned Releases', description='Select planned releases for this story'))))
finalizeATCTSchema(XPointStorySchema)
XPointStorySchema['description'].widget.visible = False

class XPointStory(ATFolder):
    """XPoint Story for a XPointProject"""
    __module__ = __name__
    schema = XPointStorySchema
    meta_type = 'XPointStory'
    portal_type = 'XPointStory'
    archetype_name = 'XP Story'
    _at_rename_after_creation = True
    __implements__ = (
     ATFolder.__implements__, IATFolder)
    log = logging.getLogger('PlonePM Story')
    security = ClassSecurityInfo()

    def vocabulary_releases(self):
        """ Return all available releases for this story.
        """
        releases = []
        for release in self.getProjectReleases():
            releases.append((release.id, release.title))

        return DisplayList(releases)

    security.declarePublic('getStoryEstimatedHours')

    def getStoryEstimatedHours(self):
        """ returns the subtotal of the estimated hours for all tasks.
        """
        tasks = self.getStoryTasks()
        estimatedSubtotal = 0
        for task in tasks:
            if task.getXptask_estimated_hours != None:
                self.log.debug('Estimated hours [%s] for task [%s]', task.xptask_estimated_hours, task.id)
                estimatedSubtotal = estimatedSubtotal + task.xptask_estimated_hours

        return estimatedSubtotal

    security.declarePublic('getStoryProgressPercent')

    def getStoryProgressPercent(self):
        """ returns the progress percent for this story, it should be the
        progress average of all its task.
        """
        tasks = self.getStoryTasks()
        averageProgress = 0
        if len(tasks) > 0:
            progressSubtotal = 0
            for task in tasks:
                if task.getXptask_progress_percent != None:
                    self.log.debug('Progress percent [%s] for task [%s]', task.xptask_progress_percent, task.id)
                    progressSubtotal = progressSubtotal + task.xptask_progress_percent

            averageProgress = progressSubtotal / len(tasks)
        return averageProgress

    security.declarePublic('getStoryTasks')

    def getStoryTasks(self):
        """ returns all tasks in this story.
      """
        return self.contentValues(filter={'portal_type': ['XPointTask']})

    security.declarePublic('getStroyMemosIssuesProposals')

    def getStoryMemosIssuesProposals(self):
        """ return all memos for this story, should includes all tasks' memo.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        cpath = ('/').join(self.getPhysicalPath())
        query = {'portal_type': ['XPointMemo', 'XPointIssue', 'XPointProposal'], 'path': cpath}
        return portal_catalog.searchResults(query)


registerType(XPointStory, PROJECTNAME)