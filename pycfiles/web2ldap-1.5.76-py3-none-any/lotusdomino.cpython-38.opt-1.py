# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/lotusdomino.py
# Compiled at: 2020-04-23 17:46:53
# Size of source mod 2**32: 2104 bytes
"""
web2ldap plugin classes for PGP key server
"""
import re
from web2ldap.app.schema.syntaxes import DynamicDNSelectList, MultilineText, SelectList, syntax_registry

class YesNoIntegerFlag(SelectList):
    __doc__ = '\n    Plugin class for flag attribute with value "yes" or "no"\n    '
    oid = 'YesNoIntegerFlag-oid'
    oid: str
    desc = '0 means no, 1 means yes'
    desc: str
    attr_value_dict = {'0':'no',  '1':'yes'}


syntax_registry.reg_at(YesNoIntegerFlag.oid, [
 '2.16.840.1.113678.2.2.2.2.4',
 '2.16.840.1.113678.2.2.2.2.18'])

class DominoCertificate(MultilineText):
    oid = 'DominoCertificate-oid'
    oid: str
    desc = 'Domino certificate'
    desc: str
    reObj = re.compile('^([A-Z0-9]{8} [A-Z0-9]{8} [A-Z0-9]{8} [A-Z0-9]{8}[\x00]?)+[A-Z0-9 ]*$')
    lineSep = b'\x00'
    mimeType = 'text/plain'
    cols = 36

    def display(self, valueindex=0, commandbutton=False) -> str:
        lines = [self._app.form.utf2display(l) for l in self._split_lines(self.av_u)]
        return '<code>%s</code>' % '<br>'.join(lines)


syntax_registry.reg_at(DominoCertificate.oid, [
 '2.16.840.1.113678.2.2.2.2.22',
 '2.16.840.1.113678.2.2.2.2.45',
 'inetpublickey'])

class CheckPassword(SelectList):
    oid = 'CheckPassword-oid'
    oid: str
    desc = ''
    desc: str
    attr_value_dict = {'0':'Do not check password',  '1':'Check password', 
     '2':'ID is locked'}


syntax_registry.reg_at(CheckPassword.oid, [
 '2.16.840.1.113678.2.2.2.2.29'])

class MailServer(DynamicDNSelectList):
    oid = 'MailServer-oid'
    oid: str
    desc = 'DN of mail server entry'
    desc: str
    ldap_url = 'ldap:///?displayname?sub?(objectClass=dominoServer)'


syntax_registry.reg_at(MailServer.oid, [
 '2.16.840.1.113678.2.2.2.2.12'])
syntax_registry.reg_syntaxes(__name__)