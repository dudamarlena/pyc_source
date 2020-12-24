# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/setuphanlders.py
# Compiled at: 2010-03-30 17:26:51
"""
miscellaneous set up steps that are not handled by GS import/export
handlers.
"""
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'
TYPES_TO_VERSION = ('PPMProject', 'PPMStory', 'PPMIteration', 'PPMUseCase')

def importVarious(context):
    """
    make sure we have membrane installed.
    """
    if context.readDataFile('plonepm_various.txt') is None:
        return
    portal = context.getSite()
    setupVersioning(portal)
    return


def setupVersioning(portal):
    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            versionable_types.append(type_id)
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)

    portal_repository.setVersionableContentTypes(versionable_types)