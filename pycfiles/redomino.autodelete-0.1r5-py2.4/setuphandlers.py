# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/setuphandlers.py
# Compiled at: 2008-03-07 08:12:45
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from redomino.autodelete.config import PROJECTNAME

def setupVarious(context):
    if context.readDataFile('redomino.autodelete_various.txt') is None:
        return
    setup_maintenance(context)
    return


def setup_maintenance(context):
    """ Adds the redomino.autodelete setup scripts, if PloneMaintenance is available """
    portal = context.getSite()
    portal_maintenance = getToolByName(portal, 'portal_maintenance', None)
    if portal_maintenance:
        scriptsholder = getattr(portal_maintenance, 'scripts', None)
        if not scriptsholder.hasObject('runAutodelete'):
            manage_addExternalMethod(scriptsholder, 'runAutodelete', 'Delete the expired content', PROJECTNAME + '.maintenance_utils', 'runAutodelete')
        else:
            ext_method = getattr(scriptsholder, 'runAutodelete')
            ext_method.reloadIfChanged()
    return