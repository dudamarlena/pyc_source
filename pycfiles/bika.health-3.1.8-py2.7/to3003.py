# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to3003.py
# Compiled at: 2014-12-12 07:13:54
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Drug', ['bika_setup_catalog'])
    pc = getToolByName(portal, 'portal_catalog', None)
    bsc = getToolByName(portal, 'bika_setup_catalog', None)
    lpc = pc(portal_type='Drug')
    for obj in lpc:
        bsc.reindexObject(obj.getObject())

    return True