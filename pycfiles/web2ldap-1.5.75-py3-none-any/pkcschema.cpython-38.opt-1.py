# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/pkcschema.py
# Compiled at: 2020-04-26 10:19:22
# Size of source mod 2**32: 1743 bytes
"""
web2ldap plugin classes for X.509 cert/CRL schema by DAASI

See also:
http://tools.ietf.org/draft/draft-ietf-pkix-ldap-pkc-schema
"""
import ldap0.filter
from web2ldap.app.schema.syntaxes import DistinguishedName, SelectList, syntax_registry

class PkcX509Issuer(DistinguishedName):
    oid = 'PkcX509Issuer-oid'
    oid: str

    def _additional_links(self):
        return [
         self._app.anchor('search',
           'Issuer', [
          (
           'dn', str(self._app.naming_context)),
          (
           'filterstr',
           '(&(objectClass=x509caCertificate)(x509subject=%s))' % (
            ldap0.filter.escape_str(self.av_u),))],
           title='Search for issuer entries')]


syntax_registry.reg_at(PkcX509Issuer.oid, [
 '1.3.6.1.4.1.10126.1.5.3.4'])

class X509KeyUsage(SelectList):
    oid = 'X509KeyUsage-oid'
    oid: str
    desc = 'Key usage extension'
    desc: str
    attr_value_dict = {'digitalSignature':'digitalSignature',  'nonRepudiation':'nonRepudiation', 
     'keyEncipherment':'keyEncipherment', 
     'dataEncipherment':'dataEncipherment', 
     'keyAgreement':'keyAgreement', 
     'keyCertSign':'keyCertSign', 
     'cRLSign':'cRLSign', 
     'encipherOnly':'encipherOnly', 
     'decipherOnly':'decipherOnly'}


syntax_registry.reg_at(X509KeyUsage.oid, [
 '1.3.6.1.4.1.10126.1.5.3.15'])
syntax_registry.reg_syntaxes(__name__)