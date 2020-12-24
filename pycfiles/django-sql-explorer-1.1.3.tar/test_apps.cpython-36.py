# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/tests/test_apps.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 693 bytes
from explorer.apps import _validate_connections
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from mock import patch

class TestApps(TestCase):

    @patch('explorer.apps._get_default')
    def test_validates_default_connections(self, mocked_connection):
        mocked_connection.return_value = 'garbage'
        self.assertRaises(ImproperlyConfigured, _validate_connections)

    @patch('explorer.apps._get_explorer_connections')
    def test_validates_all_connections(self, mocked_connections):
        mocked_connections.return_value = {'garbage1':'in',  'garbage2':'out'}
        self.assertRaises(ImproperlyConfigured, _validate_connections)