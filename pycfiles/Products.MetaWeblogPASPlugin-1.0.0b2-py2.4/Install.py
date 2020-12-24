# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\MetaWeblogPASPlugin\Extensions\Install.py
# Compiled at: 2008-04-09 20:30:40
from StringIO import StringIO
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.CMFCore.utils import getToolByName
from Products.MetaWeblogPASPlugin import config

def install(self):
    """Install the MetaWeblog credential extraction PAS plugin.
    """
    out = StringIO()
    pas = getToolByName(self, 'acl_users')
    dispatcher = pas.manage_addProduct['MetaWeblogPASPlugin']
    dispatcher.manage_addMetaWeblogCredentialPlugin(config.PLUGIN_ID, config.PLUGIN_TITLE)
    print >> out, "'%s' plugin added to acl_users." % config.PLUGIN_ID
    plugins = pas.plugins
    plugins.activatePlugin(IExtractionPlugin, config.PLUGIN_ID)
    print >> out, "'%s' plugin activated." % config.PLUGIN_ID
    print >> out, 'Successfully installed %s.' % config.PROJECTNAME
    return out.getvalue()


def uninstall(self):
    """Uninstall the PAS plugin.
    """
    out = StringIO()
    pas = getToolByName(self, 'acl_users')
    pas.plugins.deactivatePlugin(IExtractionPlugin, config.PLUGIN_ID)
    print >> out, "'%s' plugin deactivated." % config.PLUGIN_ID
    pas.manage_delObjects(ids=[config.PLUGIN_ID])
    print >> out, "'%s' plugin removed from acl_users." % config.PLUGIN_ID
    print >> out, 'Successfully uninstalled %s.' % config.PROJECTNAME
    return out.getvalue()