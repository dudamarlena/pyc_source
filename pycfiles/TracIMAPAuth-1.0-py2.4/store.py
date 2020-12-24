# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/imapauth/store.py
# Compiled at: 2007-08-28 01:00:32
import imaplib
from trac.core import *
from trac.config import Option, IntOption, BoolOption
from acct_mgr.api import IPasswordStore

class IMAPStore(Component):
    """An AccountManager backend to use IMAP."""
    __module__ = __name__
    server_host = Option('imap', 'server', default='localhost', doc='Server to use for IMAP connection')
    server_port = IntOption('imap', 'port', default=143, doc='Port to use for IMAP connection')
    use_ssl = BoolOption('imap', 'ssl', default=False, doc='Should the connection use SSL')
    implements(IPasswordStore)

    def check_password(self, user, password):
        try:
            cls = {False: imaplib.IMAP4, True: imaplib.IMAP4_SSL}[self.use_ssl]
            m = cls(self.server_host, self.server_port)
            m.login(user, password)
            return True
        except imaplib.IMAP4.error:
            return False