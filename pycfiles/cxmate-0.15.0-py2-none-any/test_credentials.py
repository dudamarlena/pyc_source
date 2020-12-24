# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/test_credentials.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Tests for the cxmanage_api.credentials module '
import unittest
from cxmanage_api.credentials import Credentials

class TestCredentials(unittest.TestCase):
    """ Unit tests for the Credentials class """

    def test_default(self):
        """ Test default Credentials object """
        creds = Credentials()
        self.assertEqual(vars(creds), Credentials.defaults)

    def test_from_dict(self):
        """ Test Credentials instantiated with a dict """
        creds = Credentials({'linux_password': 'foo'})
        expected = dict(Credentials.defaults)
        expected['linux_password'] = 'foo'
        self.assertEqual(vars(creds), expected)

    def test_from_kwargs(self):
        """ Test Credentials instantiated with kwargs """
        creds = Credentials(linux_password='foo')
        expected = dict(Credentials.defaults)
        expected['linux_password'] = 'foo'
        self.assertEqual(vars(creds), expected)

    def test_from_credentials(self):
        """ Test Credentials instantiated with other Credentials """
        creds = Credentials(Credentials(linux_password='foo'))
        expected = dict(Credentials.defaults)
        expected['linux_password'] = 'foo'
        self.assertEqual(vars(creds), expected)

    def test_fails_on_invalid(self):
        """ Test that we don't allow unrecognized credentials """
        with self.assertRaises(ValueError):
            Credentials({'desire_to_keep_going': 'Very Low'})
        with self.assertRaises(ValueError):
            Credentials(magical_mystery_cure='Writing silly strings!')