# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/service.py
# Compiled at: 2012-05-29 09:38:43
from copy import deepcopy
from five import grok
from zope.interface import Interface, invariant, Invalid
from zope import schema
from zope.component import getUtility
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from zExceptions import Redirect
from plone.registry.interfaces import IRegistry
from plone.cachepurging.interfaces import ICachePurgingSettings
from zeam.form.base.datamanager import BaseDataManager
from zeam.form.base import Actions
from zeam.form.silva import form as silvaforms
from zeam.form.ztk.actions import EditAction
from silva.core.services.base import SilvaService
from silva.core import conf as silvaconf
from .interfaces import IPurgingService

class PurgingService(SilvaService):
    """This service contains the configuration for issuing PURGE requests to
       frontend caching servers on publishing events for complex vhosting
       situations.
    """
    meta_type = 'Silva Purging Service'
    grok.implements(IPurgingService)
    silvaconf.icon('broom.png')
    default_service_identifier = 'service_purging'
    manage_options = ({'label': 'Manage', 'action': 'managepurging'},) + SilvaService.manage_options

    def __init__(self, id):
        super(PurgingService, self).__init__(id)
        self._path_mapping = {}
        self._enabled = False

    def set_path_mappings(self, new_mappings):
        """new_mappings is a dictionary in the format:
        {('','silva','sub'):['/path/to/replace/key/with', '/other/path']}
        
        The key of the mapping is the tuple representing the path to the 
        virtual host root.  The value is a list of paths to replace the
        vhroot with.  Typically a configuration might have two in this list, e.g.
        one for http and one for https.
        """
        self._path_mapping = new_mappings

    def set_enabled(self, switch):
        """Enable path mapping translations."""
        self._enabled = not not switch

    def get_enabled(self):
        return self._enabled

    def get_path_mappings(self):
        return deepcopy(self._path_mapping)


class ManageMain(grok.View):
    """Redirects the manage_main zmi screen to manage_purging
    """
    grok.context(IPurgingService)
    grok.name('manage_main')

    def render(self):
        raise Redirect(self.context.absolute_url() + '/managepurging')


registry_map = {'enabled': 'plone.cachepurging.interfaces.ICachePurgingSettings.enabled', 
   'cachingProxies': 'plone.cachepurging.interfaces.ICachePurgingSettings.cachingProxies', 
   'domains': 'plone.cachepurging.interfaces.ICachePurgingSettings.domains', 
   'virtualHosting': 'plone.cachepurging.interfaces.ICachePurgingSettings.virtualHosting'}

class PurgingDataManager(BaseDataManager):
    """Custom data manager to convert the "caching_servers" value to/from
       a string with newlines into a set.  Since neither zope.schema nor
       zeam.ztk.widgets appears to have a "Lines" field! Bah!
       
       Correction - according to sylvain, there is a 'lines' widget (use mode=lines),
       but it won't decompose rich lines (e.g. into a 2-tuple).  The "correct"
       way would be to develop a nice widget and widget extractor to represent 
       this data, but that's too much work! (though I wish I just knew how to
       do it)
    """

    def __init__(self, content):
        super(PurgingDataManager, self).__init__(content)
        self.reg = getUtility(IRegistry, context=content)

    def get(self, id):
        """If the key is in the registry_map, pull it from plone.registry.
           If it's for path_mapping, convert it to a multi-line string
           If it's for enabled, just return it.
        """
        if id in registry_map:
            return self.reg[registry_map[id]]
        if id == 'path_mapping':
            value = []
            for (path, v) in self.content._path_mapping.items():
                path = ('/').join(path)
                for _map in v:
                    value.append(path + ' ' + _map)

            return ('\r\n').join(value)
        if id == 'use_path_mapping':
            return self.content.get_enabled()

    def set(self, id, value):
        """Set the plone.registry key OR set enabled OR extract the
           data out of the textarea for the path mapping.
        """
        if id in registry_map:
            self.reg[registry_map[id]] = value
        elif id == 'path_mapping':
            if not value:
                return
            mapping = {}
            for line in value.split('\r\n'):
                (path, _map) = line.split()
                if len(path) > 1 and path[(-1)] == '/':
                    path = path[:-1]
                path = tuple(path.split('/'))
                mapping.setdefault(path, set()).add(_map)

            self.content._path_mapping = mapping
        elif id == 'use_path_mapping':
            self.content.set_enabled(value)


class IPurgingSchema(Interface):
    """ Describes fields for managing the purging service.  Mostly, this 
        interface contains the path mapping/translations, and a redefinition
        of the ICacheSettings virtualHosting field, with a more appropriate
        description.
    
        The form puts composes this interface AND some of the schema from
        plone.cachepurging.interfaces.ICacheSettings.
    """
    use_path_mapping = schema.Bool(title='Use Path Translations', description='Path Translations are an extension to plone.cachepurging which enable complex non-root-based vhosting, e.g. a vhost rooted in a subfolder of a silva root. For simple vhost configurations (e.g. a single vhost rooted at a silva root), use the domains settings below. Check  this box if you want to use path translations, and configure the translations below.', required=False)
    path_mapping = schema.Text(title='Path Translations', description="List of virtual host translations, one per line.  Each line has the vh root + ' ' + path to replace vh root.  E.g.: '/silva/www /VirtualHostBase/http/www.example.edu:80/silva/www/VirtualHostRoot'.  The same vh root path can be listed multiple times (to account for different domains, ports,  or http and https).", required=False)
    virtualHosting = schema.Bool(title='Use domain translations', description="In situations where the virtualhost root is the silva root, plone.cachepurging's virtualhosting / domains support may be used.  Supply the domains below, one per line, e.g. http://example.com:80 and https://example.com:443 .  PURGE urls will be generated with paths relative to the Silva root.", required=False)

    @invariant
    def check_path_mapping(data):
        if data.use_path_mapping and not data.path_mapping:
            raise Invalid('Use Path Mapping set, but no path translations specified.')


class ManagePurging(silvaforms.ZMIForm):
    """ Form to manage the purging server configuration.
    
        The form's fields come from IPurgingSchema and also ICachePurging.
        We use a custom data manager to get and store the data across the
        service and the registry.
    """
    grok.context(IPurgingService)
    grok.require('zope2.ViewManagementScreens')
    label = 'Manage Purging Configuration'
    description = 'Form to manage the purging server configuration.'
    ignoreContent = False
    fields = silvaforms.Fields(ICachePurgingSettings['enabled'], ICachePurgingSettings['cachingProxies'], IPurgingSchema, ICachePurgingSettings['domains'])
    actions = Actions(EditAction(title='Save Configuration'))
    dataManager = PurgingDataManager
    prefix = 'purging'