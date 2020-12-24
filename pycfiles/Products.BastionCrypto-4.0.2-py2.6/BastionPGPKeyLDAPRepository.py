# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/BastionPGPKeyLDAPRepository.py
# Compiled at: 2012-03-06 02:26:51
"""$id$"""
__version__ = '$Revision: 62 $'[11:-2]
import AccessControl, os, sys, re, tempfile, ldap, commands, time, transaction
from AccessControl import getSecurityManager, ClassSecurityInfo
from AccessControl.Permissions import view, change_configuration
from Products.PythonScripts.standard import url_quote
from Products.ZLDAPMethods.LM import LDAPFilter
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from BastionPGPKeyRepBase import BastionPGPKeyRepBase
from BastionPGPKey import BastionPGPKey
valid_fields = re.compile('(\\w+=\\w+)')
add_wildcard = re.compile('(\\w+=)(\\w+)')
manage_addBastionPGPKeyLDAPRepositoryForm = PageTemplateFile('zpt/add_pgp_ldap', globals())

def manage_addBastionPGPKeyLDAPRepository(self, connection, directory='/tmp', title='', REQUEST=None):
    """ wrapper for an OpenPGP Public Key """
    self._setObject('pks', BastionPGPKeyLDAPRepository('pks', title, directory, connection))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)
    else:
        return 0


class BastionPGPKeyLDAPRepository(BastionPGPKeyRepBase):
    """ wrapper for an OpenPGP Public Key """
    meta_type = portal_type = 'BastionPGPKeyLDAPRepository'
    _security = ClassSecurityInfo()
    manage_config = PageTemplateFile('zpt/config_ldap', globals())

    def __init__(self, id, title, directory, connection):
        BastionPGPKeyRepBase.__init__(self, id, title, directory)
        self._connection = connection

    _security.declarePrivate('manage_afterAdd')

    def manage_afterAdd(self, item, container):
        self._server_info = LDAPFilter('server_info', '', self._connection, 'SUBTREE', self._getDN(), 'baseKeySpaceDN, Software, Version', '(cn=PGPServerInfo)')
        try:
            self.server_info()
        except:
            raise AssertionError, 'PGPServerInfo not found in SUBTREE search of connection!'

    _security.declareProtected(view, 'server_info')

    def server_info(self, REQUEST=None):
        """ cached server information ... """
        if not hasattr(self, '_v_server_info'):
            self._v_server_info = self._server_info()[0]
        return self._v_server_info

    _security.declareProtected(view, 'connection_id')

    def connection_id(self):
        return self._connection

    def manage_edit(self, directory, connection, title='', REQUEST=None):
        BastionPGPRepBase.manage_edit(self, title, directory)
        if connection != self._connection_id:
            try:
                self._connection_id = connection
                self.manage_afterAdd(self, self, self.aq_parent)
            except:
                transaction.get().abort()
                if REQUEST:
                    REQUEST.set('manage_tabs_message', 'Connection Failure')
                    REQUEST.set('management_view', 'Configuration')
                    return self.manage_config(self, REQUEST)
                raise

    def _getConn(self):
        if hasattr(self, '_v_conn'):
            return self._v_conn._connection()
        for conn in self.superValues('LDAP Connection'):
            if conn.getId() == self._connection:
                self._v_conn = conn
                break

        assert hasattr(self, '_v_conn'), "Can't find LDAP Connection!!"
        return self._v_conn._connection()

    def _getDN(self):
        if hasattr(self, '_v_dn'):
            return self._v_dn
        for conn in self.superValues('LDAP Connection'):
            if conn.getId() == self._connection:
                self._v_dn = conn.getDN()
                return self._v_dn

    def _addkey(self, key):
        slapd = self._getConn()
        cn = key.pgpKeyId()
        if len(slapd.search_s(str(self.server_info().baseKeySpaceDN), ldap.SCOPE_SUBTREE, '(pgpKeyId=%s)' % cn, [])):
            raise AssertionError, 'hmmm revokation etc not yet implemented ...'
        try:
            attrs = [
             (
              'objectClass', ['pgpKey']),
             (
              'pgpKey', [key.pgpKey()]),
             (
              'pgpKeyId', [cn]),
             (
              'pgpUserId', [key.pgpUserId()])]
            slapd.add_s('cn=%s, %s' % (cn, str(self.server_info().baseKeySpaceDN)), attrs)
        except Exception, e:
            raise

    def _getkey(self, id):
        slapd = self._getConn()
        resultseq = slapd.search_s(str(self.server_info().baseKeySpaceDN), ldap.SCOPE_SUBTREE, '(pgpKeyId=%s)' % id, ('pgpKey', ))
        try:
            return resultseq[0][1]['pgpKey'][0]
        except:
            pass

    def _getkeys(self, search_criteria):
        """
        search LDAP Directory for keys
        """
        slapd = self._getConn()
        match = valid_fields.search(search_criteria)
        if not match:
            return
        filter = map(lambda x: add_wildcard.sub('pgpUserId=*\\2*', x), match.groups())
        if len(filter) > 1:
            filter = '(&%s)' % reduce(lambda x, y: '(%s)%s' % (x, y), filter)
        else:
            filter = '(%s)' % filter[0]
        resultseq = slapd.search_s(str(self.server_info().baseKeySpaceDN), ldap.SCOPE_SUBTREE, filter, [
         'pgpKey'])
        return map(lambda x: BastionPGPKey(x[1]['pgpKey'][0]), resultseq)


AccessControl.class_init.InitializeClass(BastionPGPKeyLDAPRepository)