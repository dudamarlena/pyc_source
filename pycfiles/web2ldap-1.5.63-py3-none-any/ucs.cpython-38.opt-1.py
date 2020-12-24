# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/ucs.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1755 bytes
"""
web2ldap plugin classes for Univention Corporate Server
"""
import bz2
from web2ldap.app.schema.syntaxes import Binary, RFC822Address, DynamicDNSelectList, MultilineText, syntax_registry
from web2ldap.app.plugins.msperson import DateOfBirth

class UniventionPolicyReference(DynamicDNSelectList):
    oid = 'UniventionPolicyReference-oid'
    oid: str
    desc = 'DN of the univentionPolicy entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=univentionPolicy)'


syntax_registry.reg_at(UniventionPolicyReference.oid, [
 '1.3.6.1.4.1.10176.1000'])
syntax_registry.reg_at(DateOfBirth.oid, [
 '1.3.6.1.4.1.10176.99'])
syntax_registry.reg_at(RFC822Address.oid, [
 '1.3.6.1.4.1.10176.1010.1.1'])

class UniventionLDAPACLData(Binary, MultilineText):
    oid = 'UniventionLDAPACLData-oid'
    oid: str
    desc = 'bzip2-ed LDAP ACL data in Univention'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        attr_value = bz2.decompress(self._av)
        attr_value_u = self._app.ls.uc_decode(attr_value)[0]
        lines = [self._app.form.utf2display(l, tab_identiation='    ') for l in self._split_lines(attr_value_u)]
        return '<p>%d bytes <em>BZ2</em> data contains %d chars:</p><pre>%s</pre>' % (
         len(self._av),
         len(attr_value_u),
         '<br>'.join(lines))


syntax_registry.reg_at(UniventionLDAPACLData.oid, [
 '1.3.6.1.4.1.10176.4202.1.22'])
syntax_registry.reg_syntaxes(__name__)