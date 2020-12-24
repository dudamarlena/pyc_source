# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/portaltwodotoh/Extensions/Install.py
# Compiled at: 2009-03-30 14:06:24
from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plonetheme.portaltwodotoh:default')
    return 'Ran all import steps.'


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plonetheme.portaltwodotoh:uninstall')
    return 'Ran all uninstall steps.'