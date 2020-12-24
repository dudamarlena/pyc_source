# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_base_auth_backend.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.backends.BaseAuthBackend."""
from __future__ import unicode_literals
import re
from reviewboard.accounts.backends import INVALID_USERNAME_CHAR_REGEX
from reviewboard.testing import TestCase

class BaseAuthBackendTests(TestCase):
    """Unit tests for reviewboard.accounts.backends.BaseAuthBackend."""

    def test_invalid_username_char_regex(self):
        """Testing BaseAuthBackend.INVALID_USERNAME_CHAR_REGEX"""
        cases = [
         ('spaces  ', 'spaces'),
         ('spa ces', 'spaces'),
         ('CASES', 'cases'),
         ('CaSeS', 'cases'),
         ('Spec!al', 'specal'),
         ('email@example.com', 'email@example.com'),
         ('da-shes', 'da-shes'),
         ('un_derscores', 'un_derscores'),
         ('mu ^lt&^ipl Es', 'multiples')]
        for orig, new in cases:
            self.assertEqual(re.sub(INVALID_USERNAME_CHAR_REGEX, b'', orig).lower(), new)