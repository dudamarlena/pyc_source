# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Organization/setuphandlers.py
# Compiled at: 2011-06-08 05:37:49
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
except ImportError:
    DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert')

TYPES_TO_VERSION = ('Organization', )

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