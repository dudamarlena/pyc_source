# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/themes/redmaple/Extensions/Install.py
# Compiled at: 2009-11-03 03:07:47
from Products.CMFCore.utils import getToolByName
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

def uninstall(portal):
    """
    we are using generic setup profiles here.
    """
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-iscorpio.themes.redmaple:uninstall')
    return 'Ran all uninstall steps.'