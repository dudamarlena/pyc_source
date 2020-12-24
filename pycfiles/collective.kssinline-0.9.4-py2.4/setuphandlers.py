# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/setuphandlers.py
# Compiled at: 2008-10-02 13:12:27
__author__ = 'Hedley Roos <hedley@upfrontsystems.co.za>'
__docformat__ = 'plaintext'
import logging
logger = logging.getLogger('kssinline: setuphandlers')
from collective.kssinline.config import PROJECTNAME
from collective.kssinline.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction

def isNotkssinlineProfile(context):
    return context.readDataFile('kssinline_marker.txt') is None


def setupHideToolsFromNavigation(context):
    """hide tools"""
    if isNotkssinlineProfile(context):
        return
    shortContext = context._profile_path.split(os.path.sep)[(-3)]
    if shortContext != 'kssinline':
        return
    site = context.getSite()
    toolnames = ['portal_kssinline']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass

            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)


def fixTools(context):
    """do post-processing on auto-installed tool instances"""
    site = context.getSite()
    tool_ids = [
     'portal_kssinline']
    for tool_id in tool_ids:
        tool = site[tool_id]
        tool.initializeArchetype()


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotkssinlineProfile(context):
        return
    shortContext = context._profile_path.split(os.path.sep)[(-3)]
    if shortContext != 'kssinline':
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    if isNotKssInlineProfile(context):
        return
    shortContext = context._profile_path.split(os.path.sep)[(-3)]
    if shortContext != 'KssInline':
        return
    site = context.getSite()


isNotKssInlineProfile = isNotkssinlineProfile