# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/v2/theme/Extensions/Install.py
# Compiled at: 2010-11-24 05:03:53
from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-v2.theme:default')
    return 'Ran all uninstall steps.'


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-v2.theme:uninstall')
    return 'Ran all uninstall steps.'