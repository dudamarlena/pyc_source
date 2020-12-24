# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMUseCase.py
# Compiled at: 2010-03-14 14:37:09
"""PPMUseCases defines a use case for a software project.
A use case could explain a funcationality from function specification.
"""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase
from iscorpio.plonepm.interfaces import IPPMUseCase
PPMUseCaseSchema = XPPMDocBase.schema.copy()
PPMUseCaseSchema['xppm_text'].widget.label = 'Use Case Text'
PPMUseCaseSchema['xppm_text'].widget.description = 'Details explain for this use case.'

class PPMUseCase(XPPMBase, XPPMDocBase):
    """ content type class for a use case.
    """
    __module__ = __name__
    schema = PPMUseCaseSchema
    meta_type = 'PPMUseCase'
    portal_type = 'PPMUseCase'
    archetype_name = 'PPMUseCase'
    __implements__ = (
     XPPMDocBase.__implements__,)
    implements(IPPMUseCase)
    xppm_id_prefix = 'uc'
    log = logging.getLogger('PlonePM PPMUseCase')
    security = ClassSecurityInfo()


registerType(PPMUseCase, PROJECTNAME)