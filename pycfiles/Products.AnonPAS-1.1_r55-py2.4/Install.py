# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/AnonPAS/Extensions/Install.py
# Compiled at: 2009-02-05 04:05:30
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.AnonPAS.config import *

def install(portal):
    out = StringIO()
    print >> out, 'Installing %s:' % PROJECTNAME
    pas = getToolByName(portal, 'acl_users')
    registry = pas.plugins
    existing = pas.objectIds()
    if PLUGIN_ID not in existing:
        anonpas = pas.manage_addProduct[PROJECTNAME]
        anonpas.manage_addAnonCookiePlugin(PLUGIN_ID, 'Anon Cookie Plugin')
        activatePluginInterfaces(portal, PLUGIN_ID, out)
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal):
    pas = getToolByName(portal, 'acl_users')
    existing = pas.objectIds()
    if PLUGIN_ID in existing:
        pas.manage_delObjects(PLUGIN_ID)