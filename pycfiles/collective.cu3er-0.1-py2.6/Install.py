# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/cu3er/Extensions/Install.py
# Compiled at: 2010-05-22 15:25:44
from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    """Run uninstall profile."""
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.cu3er:uninstall')
    setup_tool.setBaselineContext('profile-Products.CMFPlone:plone')
    return 'Ran all uninstall steps.'