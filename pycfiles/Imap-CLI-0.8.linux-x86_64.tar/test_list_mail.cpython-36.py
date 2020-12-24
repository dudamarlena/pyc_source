# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_list_mail.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 1218 bytes
"""Test helpers"""
import imaplib, sys, unittest
from imap_cli import const
from imap_cli import list_mail
from imap_cli import tests

class ListMailTests(unittest.TestCase):

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_list_command(self):
        const.DEFAULT_CONFIG_FILE = 'config-example.ini'
        sys.argv = [
         'imap-cli-list']
        if not list_mail.main() == 0:
            raise AssertionError
        else:
            sys.argv = [
             'imap-cli-list', '--config-file=config-example.ini']
            assert list_mail.main() == 0
            sys.argv = [
             'imap-cli-list', '--config-file=config-imaginary-file.ini']
            assert list_mail.main() == 1
            sys.argv = [
             'imap-cli-list', '--format="{from} -> {to}"']
            assert list_mail.main() == 0
            sys.argv = [
             'imap-cli-list', '-l', '2']
            assert list_mail.main() == 0
            sys.argv = [
             'imap-cli-list', '-l', 'a']
            assert list_mail.main() == 1
            sys.argv = [
             'imap-cli-list', '-l', '0']
            assert list_mail.main() == 1
            sys.argv = [
             'imap-cli-list', '-v']
            assert list_mail.main() == 0
            sys.argv = [
             'imap-cli-list', '--thread']
            assert list_mail.main() == 0