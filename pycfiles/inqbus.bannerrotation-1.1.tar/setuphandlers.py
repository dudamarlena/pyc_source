# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.bannerrotation/inqbus/bannerrotation/setuphandlers.py
# Compiled at: 2011-04-29 09:06:21
__docformat__ = 'epytext'
from Products.CMFCore.utils import getToolByName

def runCustomCode(site):
    """ Run custom add-on product installation code to modify Plone site object and others

    @param site: Plone site
    """
    if 'banners' not in site.objectIds():
        site.invokeFactory('Folder', 'banners')
        workflowTool = getToolByName(site, 'portal_workflow')
        workflowTool.doActionFor(site.banners, 'publish')
        site.banners.setTitle('Banners')
        site.banners.setExcludeFromNav(True)
        site.banners.reindexObject()


def setupVarious(context):
    """
    @param context: Products.GenericSetup.context.DirectoryImportContext instance
    """
    if context.readDataFile('inqbus.bannerrotation.marker.txt') is None:
        return
    else:
        portal = context.getSite()
        runCustomCode(portal)
        return