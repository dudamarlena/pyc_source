# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/todd/github/python-email-split/email_split/test/test.py
# Compiled at: 2016-02-03 20:36:14
from unittest import TestCase
from email_split import email_split

class TestEmailSplitFunction(TestCase):

    def test_top_level_domain(self):
        """
        email-split splitting an email with a top-level domain
            returns the local part
            returns the domain part
        """
        email = email_split('todd@underdog.io')
        self.assertEqual(email.local, 'todd')
        self.assertEqual(email.domain, 'underdog.io')

    def test_subdomain(self):
        """
        email-split splitting an email on a subdomain
            returns the local part
            returns the domain part (including subdomain)
        """
        email = email_split('you@are.super.cool')
        self.assertEqual(email.local, 'you')
        self.assertEqual(email.domain, 'are.super.cool')