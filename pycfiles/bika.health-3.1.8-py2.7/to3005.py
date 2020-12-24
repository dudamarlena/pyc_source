# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to3005.py
# Compiled at: 2014-12-12 07:13:54
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

def upgrade(tool):
    """ HEALTH-105 Case syndromic classifications site eror in setup
    """
    portal = aq_parent(aq_inner(tool))
    portal_catalog = getToolByName(portal, 'portal_catalog')
    typestool = getToolByName(portal, 'portal_types')
    setup = portal.portal_setup
    setup.runImportStepFromProfile('profile-bika.health:default', 'typeinfo')
    setup.runImportStepFromProfile('profile-bika.health:default', 'controlpanel')
    setup.runImportStepFromProfile('profile-bika.health:default', 'factorytool')
    setup.runImportStepFromProfile('profile-bika.health:default', 'propertiestool')
    setup.runImportStepFromProfile('profile-bika.health:default', 'cssregistry')
    portal = aq_parent(aq_inner(tool))
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('CaseSyndromicClassification', ['bika_setup_catalog'])
    pc = getToolByName(portal, 'portal_catalog', None)
    bsc = getToolByName(portal, 'bika_setup_catalog', None)
    lpc = pc(portal_type='CaseSyndromicClassification')
    for obj in lpc:
        bsc.reindexObject(obj.getObject())

    return True