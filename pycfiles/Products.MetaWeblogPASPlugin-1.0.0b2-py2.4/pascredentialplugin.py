# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\MetaWeblogPASPlugin\pascredentialplugin.py
# Compiled at: 2008-04-09 20:30:44
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
manage_addMetaWeblogCredentialPluginForm = PageTemplateFile('www/metaweblogAdd', globals(), __name__='manage_addMetaWeblogCredentialPluginForm')

def manage_addMetaWeblogCredentialPlugin(dispatcher, id, title=None, REQUEST=None):
    """Add a MetaWeblogCredentialPlugin to a Pluggable Auth Service.
    """
    obj = MetaWeblogCredentialPlugin(id, title)
    dispatcher._setObject(obj.getId(), obj)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message=MetaWeblogCredentialPlugin+added.' % dispatcher.absolute_url())
    return


class MetaWeblogCredentialPlugin(BasePlugin):
    """PAS plugin for extracting credentials supplied by a MetaWeblog client.
    """
    __module__ = __name__
    meta_type = 'MetaWeblogCredentialPlugin'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    security.declarePrivate('extractCredentials')

    def extractCredentials(self, request):
        try:
            login = request.args[1]
            password = request.args[2]
            return {'login': login, 'password': password}
        except IndexError:
            return {}


classImplements(MetaWeblogCredentialPlugin, IExtractionPlugin)
InitializeClass(MetaWeblogCredentialPlugin)