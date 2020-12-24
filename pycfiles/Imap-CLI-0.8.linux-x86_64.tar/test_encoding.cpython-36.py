# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_encoding.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 539 bytes
"""Test encoding helpers"""
import unittest
from imap_cli import string

class ImapUTF7Test(unittest.TestCase):
    encoded_string = '&AN8A7A-g T&AOo-st &A8kA7g-th spe&AOc-i&AOQ-l ch&AOIDwA-'
    decoded_string = 'ßìg Têst ωîth speçiäl châπ'

    def test_encode(self):
        assert string.decode(self.encoded_string) == self.decoded_string

    def test_decode(self):
        assert string.encode(self.decoded_string) == self.encoded_string