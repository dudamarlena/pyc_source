# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/ATMediaPage/exportimport.py
# Compiled at: 2010-06-03 12:11:01
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
from Products.CMFPlone.interfaces import IPropertiesTool
TYPES_TO_VERSION = ('MediaPage', )

def configureKupu(kupu):

    def addKupuResource(resourceType, portalType):
        resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
        if portalType not in resourceList:
            resourceList.append(portalType)
            kupu.addResourceType(resourceType, tuple(resourceList))

    addKupuResource('linkable', 'MediaPage')
    addKupuResource('containsanchors', 'MediaPage')
    addKupuResource('collection', 'MediaPage')


def setVersionedTypes(context):
    portal_repository = getToolByName(context, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            versionable_types.append(type_id)
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)

    portal_repository.setVersionableContentTypes(versionable_types)


def import_various(context):
    if not context.readDataFile('Products.ATMediaPage.txt'):
        return
    else:
        site = context.getSite()
        kupu = getToolByName(site, 'kupu_library_tool', None)
        if kupu is not None:
            configureKupu(kupu)
        setVersionedTypes(site)
        return