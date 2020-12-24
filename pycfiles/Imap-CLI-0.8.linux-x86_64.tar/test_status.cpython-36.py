# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_status.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 1600 bytes
"""Test helpers"""
import imaplib, unittest, imap_cli
from imap_cli import tests

class StatusTest(unittest.TestCase):

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_status(self):
        self.imap_account = imaplib.IMAP4_SSL()
        statuses = list(imap_cli.status(self.imap_account))
        for directory_status in statuses:
            assert directory_status == {'directory':'Δiπectòrÿ_ñämé',  'unseen':'0', 
             'count':'1', 
             'recent':'1'}

        assert len(statuses) == 2

    def test_status_with_wrong_imap_call(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.fail = True
        for directory_status in imap_cli.status(self.imap_account):
            assert directory_status == {'directory':'Δiπectòrÿ_ñämé',  'unseen':'0', 
             'count':'1',  'recent':'1'}

    def test_status_with_error_imap_response(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.error = True
        statuses = list(imap_cli.status(self.imap_account))
        for directory_status in statuses:
            assert directory_status == {'directory':'Δiπectòrÿ_ñämé',  'unseen':'0', 
             'count':'1',  'recent':'1'}

        assert len(statuses) == 0