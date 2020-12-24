# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/borg/supergroup/setuphandlers.py
# Compiled at: 2008-04-03 19:11:20
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from borg.supergroup.config import PLUGIN_NAME
from borg.supergroup.plugin import manage_addSuperGroupProvider

def install_plugin(context):
    """Install and prioritize the super group PAS plug-in
    """
    if context.readDataFile('borg.supergroup_various.txt') is None:
        return
    portal = context.getSite()
    out = StringIO()
    uf = getToolByName(portal, 'acl_users')
    existing = uf.objectIds()
    if PLUGIN_NAME not in existing:
        manage_addSuperGroupProvider(uf, PLUGIN_NAME)
        activatePluginInterfaces(portal, PLUGIN_NAME, out)
    else:
        print >> out, '%s already installed' % PLUGIN_NAME
    context.getLogger('borg.supergroup').info(out.getvalue())
    return