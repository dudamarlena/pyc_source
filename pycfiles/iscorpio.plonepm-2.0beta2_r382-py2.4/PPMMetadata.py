# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMMetadata.py
# Compiled at: 2010-03-08 22:25:16
"""PPMResponse defines a """
__docformat__ = 'plaintext'
import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.interfaces import IPPMMetadata
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'
PPMMetadataSchema = ATCTContent.schema.copy() + Schema((StringField('xppm_metadata_type', vocabulary='vocabulary_metadataTypes', widget=SelectionWidget(label='Metadata Type', description='Set up the type for your metadata', format='select')),))
finalizeATCTSchema(PPMMetadataSchema)

class PPMMetadata(XPPMBase, ATCTContent, HistoryAwareMixin):
    """
    a metadata for PPM Project.
    """
    __module__ = __name__
    schema = PPMMetadataSchema
    meta_type = 'PPMMetadata'
    portal_type = 'PPMMetadata'
    archetypes_type = 'PPMMetadata'
    __implements__ = (
     ATCTContent.__implements__, HistoryAwareMixin.__implements__)
    implements(IPPMMetadata)
    xppm_id_prefix = 'xpm'
    log = logging.getLogger('PlonePM PPMMetadata')
    security = ClassSecurityInfo()

    def vocabulary_metadataTypes(self):
        """ return all metadata types as a vocabulary.
        """
        return DisplayList([('priority', 'Artifact Priority'), ('category', 'Artifact Category'), ('status', 'Artifact Status'), ('tag', 'Artifact Tag')])


registerType(PPMMetadata, PROJECTNAME)