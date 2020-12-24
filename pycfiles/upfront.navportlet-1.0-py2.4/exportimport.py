# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/exportimport.py
# Compiled at: 2010-10-13 15:04:43
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.CMFCore.utils import getToolByName

def importNavigationCatalog(context):
    """Import navigation catalog.
    """
    site = context.getSite()
    tool = getToolByName(site, 'nav_catalog')
    importObjects(tool, '', context)


def exportNavigationCatalog(context):
    """Export navigation catalog.
    """
    site = context.getSite()
    tool = getToolByName(site, 'nav_catalog', None)
    if tool is None:
        logger = context.getLogger('nav_catalog')
        logger.info('Nothing to export.')
        return
    exportObjects(tool, '', context)
    return