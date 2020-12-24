# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/Extensions/Install.py
# Compiled at: 2010-08-19 06:54:20
from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.contentmigrationui:default')
    return 'Ran all import steps.'


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.contentmigrationui:uninstall')
    return 'Ran all uninstall steps.'