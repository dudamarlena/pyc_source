# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMFuncReq.py
# Compiled at: 2009-09-22 09:44:50
"""PPMFuncReq defines a function requirment for a software project."""
__docformat__ = 'plaintext'
import logging
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase
PPMFuncReqSchema = XPPMDocBase.schema.copy()
PPMFuncReqSchema['xppm_text'].widget.label = 'Function Requirement Text'
PPMFuncReqSchema['xppm_text'].widget.description = 'The details explain of the function requirement.'
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

class PPMFuncReq(XPPMBase, XPPMDocBase):
    """ content type for a function requirement.
    """
    __module__ = __name__
    schema = PPMFuncReqSchema
    meta_type = 'PPMFuncReq'
    portal_type = 'PPMFuncReq'
    archetype_name = 'PPMFuncReq'
    __implements__ = (
     XPPMDocBase.__implements__,)
    xppm_id_prefix = 'fr'
    log = logging.getLogger('PlonePM PPMFuncReq')


registerType(PPMFuncReq, PROJECTNAME)