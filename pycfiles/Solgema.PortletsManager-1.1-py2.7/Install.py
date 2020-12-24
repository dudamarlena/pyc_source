# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/Extensions/Install.py
# Compiled at: 2011-09-02 07:59:09
from Products.CMFCore.utils import getToolByName
import transaction
from zope.component import getUtility, getAdapters, getMultiAdapter, getSiteManager
from plone.portlets.interfaces import IPortletManager
from zope.interface import Interface
from zope.component import getSiteManager
from plone.portlets.interfaces import IPortletManager, IPortletRetriever
from plone.app.portlets.exportimport.interfaces import IPortletAssignmentExportImportHandler
EXTENSION_PROFILES = ('Solgema.PortletsManager:default', )

def install(portal, reinstall=False):
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    portal_setup = getToolByName(portal, 'portal_setup')
    if not reinstall:
        leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        leftColumn.listAllManagedPortlets = []
        rightColumn.listAllManagedPortlets = []
    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Solgema.PortletsManager:uninstall')
    leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
    rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
    if hasattr(leftColumn, 'listAllManagedPortlets'):
        del leftColumn.listAllManagedPortlets
    if hasattr(rightColumn, 'listAllManagedPortlets'):
        del rightColumn.listAllManagedPortlets
    sm = getSiteManager(context=portal)
    sm.unregisterAdapter(required=(Interface, IPortletManager), provided=IPortletRetriever)
    sm.unregisterAdapter(required=(Interface,), provided=IPortletAssignmentExportImportHandler)
    return 'Imported uninstall profile.'