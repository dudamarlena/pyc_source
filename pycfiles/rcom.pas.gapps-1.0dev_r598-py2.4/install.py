# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcom/pas/gapps/install.py
# Compiled at: 2008-07-07 16:53:53
from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin
import plugin
manage_add_gapps_form = PageTemplateFile('browser/add_plugin', globals(), __name__='manage_add_gapps_form')

def manage_add_gapps_helper(dispatcher, id, title=None, REQUEST=None):
    """ Add an gapps Helper to the PluggableAuthentication Service.
    """
    sp = plugin.GappsHelper(id, title)
    dispatcher._setObject(sp.getId(), sp)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message=gappsHelper+added.' % dispatcher.absolute_url())
    return


def register_gapps_plugin():
    try:
        registerMultiPlugin(plugin.GappsHelper.meta_type)
    except RuntimeError:
        pass


def register_gapps_plugin_class(context):
    context.registerClass(plugin.GappsHelper, permission=manage_users, constructors=(manage_add_gapps_form, manage_add_gapps_helper), visibility=None, icon='browser/icon.gif')
    return