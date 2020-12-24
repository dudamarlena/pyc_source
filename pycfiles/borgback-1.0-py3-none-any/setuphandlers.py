# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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