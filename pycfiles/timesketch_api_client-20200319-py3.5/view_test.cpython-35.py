# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/view_test.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 1341 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import unittest, mock
from . import client
from . import view as view_lib
from . import test_lib

class ViewTest(unittest.TestCase):
    __doc__ = 'Test View object.'

    @mock.patch('requests.Session', test_lib.mock_session)
    def setUp(self):
        """Setup test case."""
        self.api_client = client.TimesketchApi('http://127.0.0.1', 'test', 'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_view(self):
        """Test View object."""
        view = self.sketch.list_views()[0]
        self.assertIsInstance(view, view_lib.View)
        self.assertEqual(view.id, 1)
        self.assertEqual(view.name, 'test')