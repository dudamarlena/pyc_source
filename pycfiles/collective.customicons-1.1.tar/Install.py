# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/cu3er/Extensions/Install.py
# Compiled at: 2010-05-22 15:25:44
from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    """Run uninstall profile."""
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.cu3er:uninstall')
    setup_tool.setBaselineContext('profile-Products.CMFPlone:plone')
    return 'Ran all uninstall steps.'