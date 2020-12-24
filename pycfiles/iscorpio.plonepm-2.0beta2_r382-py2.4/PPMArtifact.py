# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMArtifact.py
# Compiled at: 2009-09-22 11:55:52
"""PPMStory defines a track item for a software project in Agile approach."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import AttributeStorage
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
PPMArtifactSchema = ATFolderSchema.copy() + Schema((TextField('xppm_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Details', description='Details description for this artifact', rows=18)), StringField('xppm_artifact_category', searchable=False, required=True, default='', vocabulary='vocabulary_categories', widget=SelectionWidget(label='Artifact Category', description='Select category for this artifact', format='select')), StringField('xppm_artifact_status', searchable=False, required=False, default='', vocabulary='vocabulary_artifactStatus', widget=SelectionWidget(label='Artifact Status', description='Select status for this artifact', format='select'), schemata='Metadata'), StringField('xppm_artifact_priority', searchable=False, required=False, default='', vocabulary='vocabulary_priorities', widget=SelectionWidget(label='Priority', description='Set the priority for this artifact', format='select'), schemata='Metadata'), StringField('xppm_artifact_story', searchable=False, required=False, vocabulary='vocabulary_allStoriesList', widget=SelectionWidget(label='Story', description='stories related to this artifact', format='select'), schemata='Metadata'), LinesField('xppm_artifact_tags', vocabulary='vocabulary_artifactTag', widget=InAndOutWidget(label='Tags', description='Please select the tags for this artifact'), schemata='Metadata'), FileField('xppm_artifact_attachment', widget=FileWidget(label='Attachment', description='You may upload a file here:'), storage=AttributeStorage(), schemata='Metadata')))
finalizeATCTSchema(PPMArtifactSchema)
PPMArtifactSchema['description'].widget.visible = False

class PPMArtifact(XPPMBase, ATFolder, HistoryAwareMixin):
    __module__ = __name__
    schema = PPMArtifactSchema
    meta_type = 'PPMArtifact'
    portal_type = 'PPMArtifact'
    archetypes_type = 'PPMArtifact'
    __implements__ = (
     ATFolder.__implements__, HistoryAwareMixin.__implements__)
    xppm_id_prefix = 'xpa'
    log = logging.getLogger('PlonePM PPMArtifact')
    _artifactChangeLog = []
    security = ClassSecurityInfo()

    def vocabulary_priorities(self):
        """ returns all priority options as a vocabulary.
        """
        return DisplayList([('', '')] + self.getMetadataTupleList('priority'))

    def vocabulary_categories(self):
        """ return all category options as a vocabulary.
        """
        return DisplayList(self.getMetadataTupleList('category'))

    def vocabulary_artifactStatus(self):
        """ return all status options as a vocabulary.
        """
        return DisplayList([('', '')] + self.getMetadataTupleList('status'))

    def vocabulary_artifactTag(self):
        """ return all tags options as a vocabulary.
        """
        return DisplayList(self.getMetadataTupleList('tag'))


registerType(PPMArtifact, PROJECTNAME)