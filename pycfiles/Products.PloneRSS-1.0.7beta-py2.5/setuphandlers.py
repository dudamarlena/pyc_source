# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/setuphandlers.py
# Compiled at: 2008-10-21 05:47:03
__author__ = 'unknown <unknown>'
__docformat__ = 'plaintext'
import logging
logger = logging.getLogger('PloneRSS: setuphandlers')
from Products.PloneRSS.config import PROJECTNAME
from Products.PloneRSS.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction

def isNotPloneRSSProfile(context):
    return context.readDataFile('PloneRSS_marker.txt') is None


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotPloneRSSProfile(context):
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """called as at the end of the setup process and the right place for your code"""
    pass