# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/Extensions/Install.py
# Compiled at: 2011-05-20 07:51:01
from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plonetheme.laboral:default')
    return 'Ran all install steps.'


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plonetheme.laboral:uninstall')
    return 'Ran all uninstall steps.'