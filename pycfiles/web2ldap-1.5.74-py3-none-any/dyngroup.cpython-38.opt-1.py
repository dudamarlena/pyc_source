# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/dyngroup.py
# Compiled at: 2020-04-20 10:59:45
# Size of source mod 2**32: 1770 bytes
"""
web2ldap plugin classes for attributes defined for so-called dynamic groups
"""
import ldap0, ldap0.ldapurl
from ldap0.dn import is_dn
from web2ldap.app.schema.syntaxes import LDAPUrl, syntax_registry

class MemberUrl(LDAPUrl):
    __doc__ = '\n    Plugin class for attribute memberUrl which contains an LDAP URI\n    specifying the group members.\n    '
    oid = 'MemberUrl-oid'
    oid: str
    desc = 'LDAP URL describing search parameters used to lookup group members'
    desc: str
    ldap_url = None

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        LDAPUrl.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def _validate(self, attrValue: bytes) -> bool:
        """
        Checks validity of membership LDAP URL.
        False if hostport part is non-empty, the search base is not a valid DN,
        or the base search to search base failed.
        """
        try:
            ldap_url = ldap0.ldapurl.LDAPUrl(attrValue.decode(self._app.ls.charset))
        except ValueError:
            return False
        else:
            search_base = ldap_url.dn
            if not is_dn(search_base) or ldap_url.hostport:
                return False
            try:
                self._app.ls.l.read_s((ldap_url.dn),
                  attrlist=(ldap_url.attrs),
                  filterstr=(ldap_url.filterstr or '(objectClass=*)'))
            except ldap0.LDAPError:
                return False
            else:
                return True


syntax_registry.reg_at(MemberUrl.oid, [
 '2.16.840.1.113730.3.1.198'])
syntax_registry.reg_syntaxes(__name__)