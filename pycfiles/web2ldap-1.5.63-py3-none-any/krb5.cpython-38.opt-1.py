# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/krb5.py
# Compiled at: 2019-11-25 07:11:31
# Size of source mod 2**32: 5996 bytes
"""
web2ldap plugin classes for Kerberos (see krb5-kdc.schema)
"""
from web2ldap.app.schema.syntaxes import BitArrayInteger, DirectoryString, OctetString, SelectList, DynamicDNSelectList, Timespan, syntax_registry
syntax_registry.reg_at(DirectoryString.oid, [
 '1.3.6.1.4.1.5322.10.1.1',
 '1.3.6.1.4.1.5322.10.1.12'])
syntax_registry.reg_at(OctetString.oid, [
 '1.3.6.1.4.1.5322.10.1.10'])

class Krb5KDCFlagsSyntax(BitArrayInteger):
    __doc__ = '\n       WITH SYNTAX            INTEGER\n    --        initial(0),             -- require as-req\n    --        forwardable(1),         -- may issue forwardable\n    --        proxiable(2),           -- may issue proxiable\n    --        renewable(3),           -- may issue renewable\n    --        postdate(4),            -- may issue postdatable\n    --        server(5),              -- may be server\n    --        client(6),              -- may be client\n    --        invalid(7),             -- entry is invalid\n    --        require-preauth(8),     -- must use preauth\n    --        change-pw(9),           -- change password service\n    --        require-hwauth(10),     -- must use hwauth\n    --        ok-as-delegate(11),     -- as in TicketFlags\n    --        user-to-user(12),       -- may use user-to-user auth\n    --        immutable(13)           -- may not be deleted\n    '
    oid = '1.3.6.1.4.1.5322.10.0.1'
    oid: str
    flag_desc_table = (('initial', 1), ('forwardable', 2), ('proxiable', 4), ('renewable', 8),
                       ('postdate', 16), ('server', 32), ('client', 64), ('invalid', 128),
                       ('require-preauth', 256), ('change-pw', 512), ('require-hwauth', 2048),
                       ('ok-as-delegate', 4096), ('user-to-user', 8192), ('immutable', 16384))


syntax_registry.reg_at(Krb5KDCFlagsSyntax.oid, [
 '1.3.6.1.4.1.5322.10.1.5'])
syntax_registry.reg_at(Timespan.oid, [
 '1.3.6.1.4.1.5322.10.1.3'])

class KrbTicketFlags(BitArrayInteger):
    oid = 'KrbTicketFlags-oid'
    oid: str
    flag_desc_table = (('DISALLOW_POSTDATED', 1), ('DISALLOW_FORWARDABLE', 2), ('DISALLOW_TGT_BASED', 4),
                       ('DISALLOW_RENEWABLE', 8), ('DISALLOW_PROXIABLE', 16), ('DISALLOW_DUP_SKEY', 32),
                       ('DISALLOW_ALL_TIX', 64), ('REQUIRES_PRE_AUTH', 128), ('REQUIRES_HW_AUTH', 256),
                       ('REQUIRES_PWCHANGE', 512), ('DISALLOW_SVR', 4096), ('PWCHANGE_SERVICE', 8192))


syntax_registry.reg_at(KrbTicketFlags.oid, [
 '2.16.840.1.113719.1.301.4.8.1'])

class KrbSearchScope(SelectList):
    oid = 'KrbSearchScope-oid'
    oid: str
    desc = 'Kerberos search scope'
    desc: str
    attr_value_dict = {'1':'ONE_LEVEL',  '2':'SUB_TREE'}


syntax_registry.reg_at(KrbSearchScope.oid, [
 '2.16.840.1.113719.1.301.4.25.1'])

class KrbPrincipalType(SelectList):
    oid = 'KrbPrincipalType-oid'
    oid: str
    desc = 'Kerberos V Principal Type (see RFC 4120, section 6.2)'
    desc: str
    attr_value_dict = {'0':'NT-UNKNOWN',  '1':'NT-PRINCIPAL', 
     '2':'NT-SRV-INST', 
     '3':'NT-SRV-HST', 
     '4':'NT-SRV-XHST', 
     '5':'NT-UID', 
     '6':'NT-X500-PRINCIPAL', 
     '7':'NT-SMTP-NAME', 
     '10':'NT-ENTERPRISE'}


syntax_registry.reg_at(KrbPrincipalType.oid, [
 '2.16.840.1.113719.1.301.4.3.1'])

class KrbTicketPolicyReference(DynamicDNSelectList):
    oid = 'KrbTicketPolicyReference-oid'
    oid: str
    desc = 'DN of a Kerberos V ticket policy entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=krbTicketPolicy)'


syntax_registry.reg_at(KrbTicketPolicyReference.oid, [
 '2.16.840.1.113719.1.301.4.40.1'])

class KrbPwdPolicyReference(DynamicDNSelectList):
    oid = 'KrbPwdPolicyReference-oid'
    oid: str
    desc = 'DN of a Kerberos V password policy entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=krbPwdPolicy)'


syntax_registry.reg_at(KrbPwdPolicyReference.oid, [
 '2.16.840.1.113719.1.301.4.36.1'])
syntax_registry.reg_at(Timespan.oid, [
 '1.2.840.113554.1.4.1.6.3',
 '1.2.840.113554.1.4.1.6.4',
 '1.3.6.1.4.1.5322.21.2.3',
 '2.16.840.1.113719.1.301.4.10.1',
 '2.16.840.1.113719.1.301.4.30.1',
 '2.16.840.1.113719.1.301.4.31.1',
 '2.16.840.1.113719.1.301.4.9.1'])
syntax_registry.reg_syntaxes(__name__)