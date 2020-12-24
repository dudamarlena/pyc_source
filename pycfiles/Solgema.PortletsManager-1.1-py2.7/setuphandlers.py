# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/setuphandlers.py
# Compiled at: 2013-06-12 05:28:34
from StringIO import StringIO
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions import StandardModifiers
from Products.CMFEditions.VersionPolicies import ATVersionOnEditPolicy
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.CMFCore import permissions
from zope.component import getUtility, getAdapters
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from plone.portlets.interfaces import IPortletManager
security = ClassSecurityInfo()

def setPortletInterface(portal, out):
    leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
    rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)


def setupSolgemaPortletsManager(context):
    """various things to do while installing..."""
    if context.readDataFile('spm_various.txt') is None:
        return
    else:
        site = context.getSite()
        jstool = getToolByName(site, 'portal_javascripts')
        jstool.cookResources()
        csstool = getToolByName(site, 'portal_css')
        csstool.cookResources()
        out = StringIO()
        return