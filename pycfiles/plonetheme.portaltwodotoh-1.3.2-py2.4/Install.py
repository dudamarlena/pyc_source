# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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