# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Person/setuphandlers.py
# Compiled at: 2011-06-08 05:39:46
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
except ImportError:
    DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert')

TYPES_TO_VERSION = ('Person', )

def setVersionedTypes(portal):
    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            versionable_types.append(type_id)
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)

    portal_repository.setVersionableContentTypes(versionable_types)


def importVarious(context):
    """Miscellanous steps import handle"""
    portal = context.getSite()
    setVersionedTypes(portal)