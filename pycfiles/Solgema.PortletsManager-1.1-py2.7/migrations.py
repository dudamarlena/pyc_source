# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/upgrades/migrations.py
# Compiled at: 2016-06-03 03:50:54
import logging
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getAdapters, getMultiAdapter
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping, IPortletAssignmentSettings
from Solgema.PortletsManager.interfaces import ISolgemaPortletAssignment

def doNothing(context):
    pass


def reinstall(context):
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.PortletsManager:default')


def upgrade06(context):
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.PortletsManager.upgrades:upgrade06')
    jstool = getToolByName(context, 'portal_javascripts')
    jstool.cookResources()
    csstool = getToolByName(context, 'portal_css')
    csstool.cookResources()


def upgrade08(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.PortletsManager.upgrades:upgrade08')


def upgrade09(context):
    portal_setup = getToolByName(context, 'portal_setup')
    site = getToolByName(context, 'portal_url').getPortalObject()
    rcolumn = getUtility(IPortletManager, name='plone.rightcolumn', context=site)
    lcolumn = getUtility(IPortletManager, name='plone.leftcolumn', context=site)
    rmanager = getMultiAdapter((site, rcolumn), IPortletAssignmentMapping)
    lmanager = getMultiAdapter((site, lcolumn), IPortletAssignmentMapping)
    rportletnames = [ v.title for v in rmanager.values() ]
    lportletnames = [ v.title for v in lmanager.values() ]
    for portlet in rmanager.values():
        IPortletAssignmentSettings(portlet).set('stopUrls', getattr(ISolgemaPortletAssignment(portlet), 'stopUrls', []))

    for portlet in lmanager.values():
        IPortletAssignmentSettings(portlet).set('stopUrls', getattr(ISolgemaPortletAssignment(portlet), 'stopUrls', []))