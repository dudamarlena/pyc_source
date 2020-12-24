# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/BastionPGPKeyRepBase.py
# Compiled at: 2012-03-06 02:26:51
"""$id$"""
__version__ = '$Revision: 62 $'[11:-2]
import AccessControl
from AccessControl.Permissions import view, change_configuration
from App.Common import rfc1123_date
from Products.CMFCore.utils import getToolByName
try:
    from Products.BastionBase.BSimpleItem import BSimpleItem as SimpleItem
except:
    from OFS.SimpleItem import SimpleItem

from OFS.PropertyManager import PropertyManager
from Products.PythonScripts.standard import url_quote
from Permissions import add_pgp_keys
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from BastionPGPKey import BastionPGPKey

class BastionPGPKeyRepBase(PropertyManager, SimpleItem):
    """
    
    The base class for key repository backends
    
    """
    __ac_permissions__ = PropertyManager.__ac_permissions__ + ((view, ('lookup', 'manage_search')), (add_pgp_keys, ('manage_addkey', 'add', 'add_bastioncrypto'))) + SimpleItem.__ac_permissions__
    _properties = PropertyManager._properties + ({'id': 'directory', 'type': 'string', 'mode': 'w'}, {'id': 'mime_type', 'type': 'string', 'mode': 'w'}, {'id': 'obfuscate_email', 'type': 'boolean', 'mode': 'w'})
    manage_options = ({'label': 'Search', 'action': 'manage_search'}, {'label': 'Add Key', 'action': 'manage_addkey'}, {'label': 'Properties', 'action': 'manage_propertiesForm'}) + SimpleItem.manage_options

    def __init__(self, id, title, directory):
        self.id = id
        self.title = title
        self.directory = directory
        self.mime_type = 'application/x-pgp'
        self.obfuscate_email = 1

    manage_search = PageTemplateFile('zpt/search', globals())
    manage_addkey = PageTemplateFile('zpt/add_key', globals())

    def all_meta_types(self):
        return (
         {'action': 'manage_addProduct/BastionCrypto/addBastionPGPKeyRecord', 'permission': 'Add BastionCryptoPGPKeyRecord', 
            'name': 'PGPKey Record', 
            'Product': 'BastionCrypto', 
            'instance': BastionPGPKeyRecord},)

    def add(self, keyfile='', keytext='', REQUEST=None):
        """ """
        if keytext == '' and keyfile == '':
            return self._error('You must provide a public key, either text or upload file!', REQUEST)
        if keytext == '':
            if keyfile.filename == '':
                return self._error('You must supply your public key file!', REQUEST)
            keytext = keyfile.read()
        key = BastionPGPKey(keytext)
        if not key.isValid():
            return self._error("Woa - this doesn't appear to be a GPG Key (%s)" % keytext, REQUEST)
        try:
            self._addkey(key)
        except Exception, e:
            return self._error(str(e), REQUEST)

        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Successfully added key')
            REQUEST.set('management_view', 'Add Key')
            return self.manage_addkey(self, REQUEST)

    def lookup(self, op='get', keyid='', REQUEST=None):
        """ download key to local machine ... """
        assert op in ('get', 'index'), 'Bad op!'
        if op == 'get':
            key = self._getkey(keyid)
            if REQUEST:
                REQUEST.RESPONSE.setHeader('Content-Type', self.mime_type)
                REQUEST.RESPONSE.write(key)
            return key
        else:
            keys = self._getkeys(keyid)
            if REQUEST:
                REQUEST.RESPONSE.setHeader('Content-Type', self.mime_type)
                REQUEST.RESPONSE.write(string.join(keys, '\n'))
            return keys

    def _error(self, msg, REQUEST=None):
        if REQUEST is None:
            raise AttributeError, msg
        else:
            REQUEST.set('management_view', 'Add Key')
            REQUEST.set('manage_tabs_message', msg)
            return self.manage_addkey(self, REQUEST)
        return

    def _addkey(self, bastionpgpkey):
        raise NotImplementedError

    def _getkey(self, keyid):
        raise NotImplementedError

    def _getkeys(self, keyids):
        raise NotImplementedError

    def add_bastioncrypto(self, REQUEST, RESPONSE):
        """
        use the bastioncrypto helper application to export your key
        """
        r = []
        r.append('url:%s' % self.absolute_url())
        key_id = getToolByName(self, 'portal_membership').getAuthenticatedMember().email
        r.append("arguments:--export --armor -u '<%s>'" % key_id)
        if REQUEST._auth[(-1)] == '\n':
            auth = REQUEST._auth[:-1]
        else:
            auth = REQUEST._auth
        r.append('auth:%s' % auth)
        r.append('cookie:%s' % REQUEST.environ.get('HTTP_COOKIE', ''))
        r.append('')
        RESPONSE.setHeader('Last-Modified', rfc1123_date())
        RESPONSE.setHeader('Content-Type', 'application/x-bastioncrypto')
        return ('\n').join(r)

    def PUT(self, REQUEST, RESPONSE):
        """
        return packet from our bastioncrypto ...
        """
        self.dav__init(REQUEST, RESPONSE)
        self.dav__simpleifhandler(REQUEST, RESPONSE, refresh=1)
        self.add(keytext=REQUEST['BODYFILE'].read())
        RESPONSE.setStatus(204)
        return RESPONSE


AccessControl.class_init.InitializeClass(BastionPGPKeyRepBase)