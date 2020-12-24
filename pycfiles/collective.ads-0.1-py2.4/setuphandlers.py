# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/setuphandlers.py
# Compiled at: 2009-01-02 05:05:21
__author__ = 'info@fourdigits.nl'
__docformat__ = 'plaintext'
import logging
logger = logging.getLogger('Ads: setuphandlers')
from collective.ads.config import PROJECTNAME
from collective.ads.config import DEPENDENCIES
from Products.CMFCore.utils import getToolByName
from collective.ads.config import TOOL_TITLE

def installGSDependencies(context):
    """Install dependend profiles."""
    dependencies = []
    if not dependencies:
        return
    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    for dependency in dependencies:
        if dependency.find(':') == -1:
            dependency += ':default'
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-%s' % dependency)
        importsteps = setup_tool.getImportStepRegistry().sortSteps()
        excludes = ['Ads-QI-dependencies', 'Ads-GS-dependencies']
        importsteps = [ s for s in importsteps if s not in excludes ]
        for step in importsteps:
            setup_tool.runImportStep(step)

        setup_tool.setImportContext(old_context)

    importsteps = setup_tool.getImportStepRegistry().sortSteps()
    filter = ['typeinfo', 'workflow', 'membranetool', 'factorytool', 'content_type_registry', 'membrane-sitemanager']
    importsteps = [ s for s in importsteps if s in filter ]
    for step in importsteps:
        setup_tool.runImportStep(step)


def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):
            logger.info('Re-Installing dependency %s:' % dependency)
            qi.reinstallProducts([dependency])
        else:
            logger.info('Installing dependency %s:' % dependency)
            qi.installProducts([dependency])


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    site = context.getSite()


def importVarious(self):
    if self.readDataFile('atadsmanager.txt') is None:
        logger.info('Return')
        return
    site = self.getSite()
    vtool = getToolByName(site, 'portal_adsadmin')
    vtool.title = TOOL_TITLE
    logger.info('portal_adsadmin = %s:' % TOOL_TITLE)
    vtool.unindexObject()
    return