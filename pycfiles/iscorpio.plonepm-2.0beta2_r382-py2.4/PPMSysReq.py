# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMSysReq.py
# Compiled at: 2009-09-22 09:45:14
"""PPMSysReq defines a system requirment for a software project."""
__docformat__ = 'plaintext'
import logging
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'
PPMSysReqSchema = XPPMDocBase.schema.copy()
PPMSysReqSchema['xppm_text'].widget.label = 'System Requirement Text'
PPMSysReqSchema['xppm_text'].widget.description = 'The details explain of the system requirement.'

class PPMSysReq(XPPMBase, XPPMDocBase):
    """ content type for a system requirement.
    """
    __module__ = __name__
    schema = PPMSysReqSchema
    meta_type = 'PPMSysReq'
    portal_type = 'PPMSysReq'
    archetype_name = 'PPMSysReq'
    __implements__ = (
     XPPMDocBase.__implements__,)
    xppm_id_prefix = 'xpsr'
    log = logging.getLogger('PlonePM PPMSysReq')


registerType(PPMSysReq, PROJECTNAME)