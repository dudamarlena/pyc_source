# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/ldapns.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1428 bytes
"""
web2ldap plugin classes for LDAP-based naming service (ldapns.schema)
"""
from web2ldap.app.schema.syntaxes import SelectList, syntax_registry

class AuthorizedService(SelectList):
    __doc__ = '\n    See https://www.iana.org/assignments/gssapi-service-names/gssapi-service-names.xhtml\n    '
    oid = 'AuthorizedService-oid'
    oid: str
    desc = 'IANA GSS-API authorized service name'
    desc: str
    attr_value_dict = {'':'', 
     'rcmd':'remote command/rlogin/telnet', 
     'imap':'mailstore access/IMAP4', 
     'pop':'maildrop access/POP3', 
     'acap':'remote configuration access/ACAP', 
     'nfs':'distributed file system protocol (NFS)', 
     'ftp':'file transfer/FTP/TFTP', 
     'ldap':'Lightweight Directory Access Protocol (LDAP)', 
     'smtp':'message transfer/SMTP', 
     'beep':'Blocks Extensible Exchange Protocol (BEEP)', 
     'mupdate':'Mailbox Update (MUPDATE) Protocol', 
     'sacred':'Secure Available Credentials (SACRED) Protocol', 
     'sieve':'ManageSieve Protocol', 
     'xmpp':'Extensible Messaging and Presence Protocol (XMPP)', 
     'nntp':'Network News Transfer Protocol (NNTP)'}


syntax_registry.reg_at(AuthorizedService.oid, [
 '1.3.6.1.4.1.5322.17.2.1'])
syntax_registry.reg_syntaxes(__name__)