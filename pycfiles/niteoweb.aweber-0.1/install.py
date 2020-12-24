# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/niteoweb.plr/src/niteoweb.aweber/src/niteoweb/aweber/Extensions/install.py
# Compiled at: 2013-02-08 04:56:13
"""Run (install and) uninstall steps for this package."""
from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    """Run uninstall steps.

    :param portal: navigation root
    :type portal: Portal object
    :rtype: string
    :returns: static string on success
    """
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-niteoweb.aweber:uninstall')
    return 'Ran all uninstall steps.'