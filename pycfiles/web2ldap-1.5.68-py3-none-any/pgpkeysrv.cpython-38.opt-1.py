# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/pgpkeysrv.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1560 bytes
"""
web2ldap plugin classes for PGP key server
"""
import re
from web2ldap.app.schema.syntaxes import DirectoryString, GeneralizedTime, PreformattedMultilineText, DynamicValueSelectList, syntax_registry
syntax_registry.reg_at(GeneralizedTime.oid, [
 '1.3.6.1.4.1.3401.8.2.17',
 '1.3.6.1.4.1.3401.8.2.22'])

class PgpKey(PreformattedMultilineText):
    oid = 'PgpKey-oid'
    oid: str
    desc = 'PGP key'
    desc: str
    reObj = re.compile('^-----BEGIN PGP PUBLIC KEY BLOCK-----[a-zA-Z0-9.: ()+/ =\n-]+-----END PGP PUBLIC KEY BLOCK-----$', re.S + re.M)
    lineSep = b'\n'
    mimeType = 'application/pgp-keys'
    cols = 64


syntax_registry.reg_at(PgpKey.oid, [
 '1.3.6.1.4.1.3401.8.2.11'])

class PgpCertID(DirectoryString):
    oid = 'PgpCertID-oid'
    oid: str
    desc = 'PGP Cert ID'
    desc: str
    reObj = re.compile('^[a-fA-F0-9]{16}$')


syntax_registry.reg_at(PgpCertID.oid, [
 '1.3.6.1.4.1.3401.8.2.12'])

class OtherPgpCertID(DynamicValueSelectList, PgpCertID):
    oid = 'OtherPgpCertID-oid'
    oid: str
    ldap_url = 'ldap:///_?pgpCertID,pgpCertID?sub?(objectClass=pgpKeyInfo)'

    def _validate(self, attrValue: bytes) -> bool:
        return PgpCertID._validate(self, attrValue)


syntax_registry.reg_at(OtherPgpCertID.oid, [
 '1.3.6.1.4.1.3401.8.2.18'])
syntax_registry.reg_syntaxes(__name__)