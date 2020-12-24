# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMResponse.py
# Compiled at: 2009-11-19 20:20:12
"""PPMResponse defines a """
import logging
from time import strftime
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import AttributeStorage
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'
__docformat__ = 'plaintext'
PPMResponseSchema = ATCTContent.schema.copy() + Schema((TextField('xppm_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Details', description='Details description for your response', rows=18)), StringField('xppm_response_category', mutator='setXppm_response_category', searchable=False, required=True, vocabulary='vocabulary_categories', widget=SelectionWidget(label='Artifact Category', description='Select new category for this artifact', format='select'), default_method='getCurrentArtifactCategory', schemata='Metadata'), StringField('xppm_response_status', mutator='setXppm_response_status', searchable=False, required=False, vocabulary='vocabulary_artifactStatus', widget=SelectionWidget(label='Artifact Status', description='Select new status for this artifact', format='select'), default_method='getCurrentArtifactStatus', schemata='Metadata'), StringField('xppm_response_priority', mutator='setXppm_response_priority', searchable=False, required=False, vocabulary='vocabulary_priorities', widget=SelectionWidget(label='Priority', description='Set the new priority for this artifact', format='select'), default_method='getCurrentArtifactPriority', schemata='Metadata'), LinesField('xppm_response_tags', mutator='setXppm_response_tags', vocabulary='vocabulary_artifactTag', widget=InAndOutWidget(label='Tags', description='Please select the tags for this artifact'), default_method='getCurrentArtifactTags', schemata='Metadata'), StringField('xppm_response_story', mutator='setXppm_response_story', searchable=False, required=False, vocabulary='vocabulary_allStoriesList', widget=SelectionWidget(label='Story', description='stories related to this artifact', format='select'), default_method='getCurrentArtifactStory', schemata='Metadata'), FileField('xppm_response_attachment', widget=FileWidget(label='Attachment', description='You may upload a file here:'), storage=AttributeStorage(), schemata='Metadata')))
finalizeATCTSchema(PPMResponseSchema)
PPMResponseSchema['description'].widget.visible = False

class PPMResponse(XPPMBase, ATCTContent, HistoryAwareMixin):
    __module__ = __name__
    schema = PPMResponseSchema
    meta_type = 'PPMResponse'
    portal_type = 'PPMResponse'
    archetypes_type = 'PPMResponse'
    __implements__ = (
     HistoryAwareMixin.__implements__, ATCTContent.__implements__)
    xppm_id_prefix = 'xpr'
    log = logging.getLogger('PlonePM PPMResponse')
    security = ClassSecurityInfo()
    security.declareProtected(permissions.View, 'getCurrentArtifactStory')

    def getCurrentArtifactStory(self):
        if self.aq_inner.aq_parent.portal_type == 'PPMArtifact':
            return self.aq_inner.aq_parent.getXppm_artifact_story()

    security.declareProtected(permissions.View, 'getCurrentArtifactPriority')

    def getCurrentArtifactPriority(self):
        if self.aq_inner.aq_parent.portal_type == 'PPMArtifact':
            return self.aq_inner.aq_parent.getXppm_artifact_priority()

    security.declareProtected(permissions.View, 'getCurrentArtifactCategory')

    def getCurrentArtifactCategory(self):
        if self.aq_inner.aq_parent.portal_type == 'PPMArtifact':
            return self.aq_inner.aq_parent.getXppm_artifact_category()

    security.declareProtected(permissions.View, 'getCurrentArtifactStatus')

    def getCurrentArtifactStatus(self):
        if self.aq_inner.aq_parent.portal_type == 'PPMArtifact':
            return self.aq_inner.aq_parent.getXppm_artifact_status()

    security.declareProtected(permissions.View, 'getCurrentArtifactTags')

    def getCurrentArtifactTags(self):
        if self.aq_inner.aq_parent.portal_type == 'PPMArtifact':
            return self.aq_inner.aq_parent.getXppm_artifact_tags()
        else:
            return []

    security.declareProtected(permissions.ModifyPortalContent, 'setXppm_response_story')

    def setXppm_response_story(self, storyNew):
        storyNow = self.getCurrentArtifactStory()
        if storyNew and storyNow != storyNew:
            self.logArtifactChanges('Story', storyNow, storyNew)
            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_story(storyNew)
            artifact.reindexObject(('getXppm_artifact_story', ))
        self.getField('xppm_response_story').set(self, storyNew)

    security.declareProtected(permissions.ModifyPortalContent, 'setXppm_response_priority')

    def setXppm_response_priority(self, priorityNew):
        priorityNow = self.getCurrentArtifactPriority()
        if priorityNew and priorityNow != priorityNew:
            self.logArtifactChanges('Priority', priorityNow, priorityNew)
            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_priority(priorityNew)
            artifact.reindexObject(('getXppm_artifact_priority', ))
        self.getField('xppm_response_priority').set(self, priorityNew)

    security.declareProtected(permissions.ModifyPortalContent, 'setXppm_response_category')

    def setXppm_response_category(self, categoryNew):
        categoryNow = self.getCurrentArtifactCategory()
        if categoryNew and categoryNow != categoryNew:
            self.logArtifactChanges('Category', categoryNow, categoryNew)
            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_category(categoryNew)
            artifact.reindexObject(('getXppm_artifact_catetory', ))
        self.getField('xppm_response_category').set(self, categoryNew)

    security.declareProtected(permissions.ModifyPortalContent, 'setXppm_response_status')

    def setXppm_response_status(self, statusNew):
        statusNow = self.getCurrentArtifactStatus()
        if statusNew and statusNow != statusNew:
            self.logArtifactChanges('Status', statusNow, statusNew)
            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_status(statusNew)
            artifact.reindexObject(('getXppm_artifact_status', ))
        self.getField('xppm_response_status').set(self, statusNew)

    security.declareProtected(permissions.ModifyPortalContent, 'setXppm_response_tags')

    def setXppm_response_tags(self, tagsNew):
        tagsNow = self.getCurrentArtifactTags()
        if tagsNow and tagsNow != tagsNew:
            artifact = self.aq_inner.aq_parent
            artifact.setXppm_artifact_tags(tagsNew)
            artifact.reindexObject(('getXppm_artifact_tags', ))
        self.getField('xppm_response_tags').set(self, tagsNew)

    def logArtifactChanges(self, name, before, after):
        artifact = self.aq_inner.aq_parent
        if not artifact._artifactChangeLog:
            artifact._artifactChangeLog = []
        changeTime = strftime('%Y-%m-%d %H:%M:%S')
        artifact._artifactChangeLog.append({'time': changeTime, 'name': name, 'before': before, 'after': after})


registerType(PPMResponse, PROJECTNAME)