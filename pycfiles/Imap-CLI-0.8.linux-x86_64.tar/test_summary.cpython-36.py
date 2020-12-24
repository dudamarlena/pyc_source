# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_summary.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 901 bytes
"""Test helpers"""
import imaplib, sys, unittest
from imap_cli import const
from imap_cli import summary
from imap_cli import tests

class FetchTest(unittest.TestCase):

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_status_command(self):
        const.DEFAULT_CONFIG_FILE = 'config-example.ini'
        sys.argv = [
         'imap-cli-status']
        if not summary.main() == 0:
            raise AssertionError
        else:
            sys.argv = [
             'imap-cli-status', '--config-file=config-example.ini']
            assert summary.main() == 0
            sys.argv = [
             'imap-cli-status',
             '--config-file=config-imaginary-file.ini']
            assert summary.main() == 1
            sys.argv = [
             'imap-cli-status', '--format="{directory:>10} {unseen}"']
            assert summary.main() == 0
            sys.argv = [
             'imap-cli-status', '-v']
            assert summary.main() == 0