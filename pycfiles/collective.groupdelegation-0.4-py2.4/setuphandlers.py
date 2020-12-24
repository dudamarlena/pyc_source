# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\groupdelegation\setuphandlers.py
# Compiled at: 2009-06-29 15:39:43
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

def isNotgroupdelegationProfile(context):
    return context.readDataFile('groupdelegation_marker.txt') is None


def importFinalSteps(context):
    """Import steps that are not handled by GS import/export handlers
    """
    if isNotgroupdelegationProfile(context):
        return
    portal = context.getSite()
    setupGroupDataDelegation(portal)


def setupGroupDataDelegation(context):
    """Property added in portal_groupdata for Group Delegation
    """
    gd_tool = getToolByName(context, 'portal_groupdata')
    if not base_hasattr(gd_tool, 'delegated_group_member_managers'):
        gd_tool._setProperty('delegated_group_member_managers', (), 'lines')