# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMFuncSpec.py
# Compiled at: 2009-09-22 09:42:55
"""PPMFuncSpec defines a function specification document for a software project."""
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'
PPMFuncSpecSchema = ATFolderSchema.copy() + Schema((FileField('xppm_fsd', required=True, searchable=True, storage=AnnotationStorage(migrate=True), widget=FileWidget(label='Document', description='The function specification docuement')),))
finalizeATCTSchema(PPMFuncSpecSchema)

class PPMFuncSpec(XPPMBase, ATFolder, HistoryAwareMixin):
    """ defines a content type for function specification docuemtn.
    """
    __module__ = __name__
    schema = PPMFuncSpecSchema
    meta_type = 'PPMFuncSpec'
    portal_type = 'PPMFuncSpec'
    archetypes_type = 'PPMFuncSpec'
    __implements__ = (
     ATFolder.__implements__, HistoryAwareMixin.__implements__)
    xppm_id_prefix = 'fsd'
    log = logging.getLogger('PlonePM FSD')
    security = ClassSecurityInfo()
    security.declarePublic('getUseCases')

    def getUseCases(self):
        """ return all use cases in the FSD.
        """
        pass


registerType(PPMFuncSpec, PROJECTNAME)