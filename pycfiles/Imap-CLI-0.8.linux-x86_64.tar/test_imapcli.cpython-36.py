# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_imapcli.py
# Compiled at: 2018-06-03 05:36:57
# Size of source mod 2**32: 2195 bytes
"""Test helpers"""
import imaplib, unittest, imap_cli
from imap_cli import tests

class ImapCLITest(unittest.TestCase):

    def setUp(self):
        imaplib.IMAP4 = tests.ImapConnectionMock()
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_change_dir(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()
        imap_cli.change_dir(self.imap_account, 'Test')

    def test_change_dir_twice(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()
        if not imap_cli.change_dir(self.imap_account, 'Test') == '1':
            raise AssertionError
        elif not imap_cli.change_dir(self.imap_account, 'INBOX') == '1':
            raise AssertionError

    def test_connect(self):
        self.imap_account = imap_cli.connect('hostname', 'username', 'password')
        assert isinstance(self.imap_account, tests.ImapConnectionMock)

    def test_connect_no_ssl(self):
        self.imap_account = imap_cli.connect('hostname', 'username', 'password',
          ssl=False)
        assert isinstance(self.imap_account, tests.ImapConnectionMock)

    def test_connect_sasl_auth(self):
        self.imap_account = imap_cli.connect('hostname', 'username', sasl_auth='XOAUTH2',
          sasl_ir='12345abcde')
        assert isinstance(self.imap_account, tests.ImapConnectionMock)

    def test_wrong_change_dir(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()
        assert imap_cli.change_dir(self.imap_account, 'NotADirectory') == -1

    def test_disconnect(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()
        imap_cli.disconnect(self.imap_account)
        assert self.imap_account.state == 'LOGOUT'

    def test_disconnect_selected_state(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()
        imap_cli.change_dir(self.imap_account, 'Test')
        imap_cli.disconnect(self.imap_account)
        assert self.imap_account.state == 'LOGOUT'