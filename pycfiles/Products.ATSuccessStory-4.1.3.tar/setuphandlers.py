# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/setuphandlers.py
# Compiled at: 2015-12-17 03:21:31
__author__ = 'Franco Pellegrini <frapell@menttes.com>'
__docformat__ = 'plaintext'
import logging
logger = logging.getLogger('ATSuccessStory: setuphandlers')
from Products.ATSuccessStory.config import PROJECTNAME
from Products.ATSuccessStory.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction

def isNotATSuccessStoryProfile(context):
    return context.readDataFile('ATSuccessStory_marker.txt') is None


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotATSuccessStoryProfile(context):
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    if isNotATSuccessStoryProfile(context):
        return
    site = context.getSite()