# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/patchfss/patch.py
# Compiled at: 2009-09-16 06:25:49
import logging
logger = logging.getLogger('atreal.patchfss')
LOG = logger.info
import os
from Products.CMFCore.utils import ContentInit
from Products.CMFCore import permissions as CCP
from Products.Archetypes.public import process_types, listTypes
from Products.CMFEditions.Modifiers import ConditionalTalesModifier
from iw.fss.modifier import manage_addModifier
from iw.fss.modifier import modifierAddForm
from iw.fss.modifier import MODIFIER_ID

def initialize(context):
    from iw.fss.config import PROJECTNAME
    from iw.fss.customconfig import ZOPETESTCASE, INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE
    if ZOPETESTCASE or os.environ.get(INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE):
        from iw.fss import examples
        dummy = examples
        (content_types, constructors, ftis) = process_types(listTypes(PROJECTNAME), PROJECTNAME)
        ContentInit('%s Content' % PROJECTNAME, content_types=content_types, permission=CCP.AddPortalContent, extra_constructors=constructors, fti=ftis).initialize(context)
    context.registerClass(ConditionalTalesModifier, MODIFIER_ID, permission=CCP.ManagePortal, constructors=(modifierAddForm, manage_addModifier), icon='modifier.gif')
    from iw.fss import modulealiases
    dummy = modulealiases
    LOG('Monkey patching iw.fss.initialize with atreal.patchfss.patch.initialize')