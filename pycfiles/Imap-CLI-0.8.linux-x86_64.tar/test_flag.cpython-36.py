# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_flag.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 609 bytes
"""Test flag module"""
import imaplib, sys, unittest
from imap_cli import const
from imap_cli import flag
from imap_cli import tests

class FlagTests(unittest.TestCase):

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_flag_cli_tools(self):
        const.DEFAULT_CONFIG_FILE = 'config-example.ini'
        sys.argv = [
         'imap-cli-flag', '-c', 'config-example.ini', '1',
         'testFlag']
        if not flag.main() == 0:
            raise AssertionError
        else:
            sys.argv = [
             'imap-cli-flag', '-u', '1', 'testFlag']
            assert flag.main() == 0