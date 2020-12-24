# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/client_test.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 1894 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import unittest, mock
from . import client
from . import sketch as sketch_lib
from . import test_lib

class TimesketchApiTest(unittest.TestCase):
    __doc__ = 'Test TimesketchApi'

    @mock.patch('requests.Session', test_lib.mock_session)
    def setUp(self):
        """Setup test case."""
        self.api_client = client.TimesketchApi('http://127.0.0.1', 'test', 'test')

    def test_fetch_resource_data(self):
        """Test fetch resource."""
        response = self.api_client.fetch_resource_data('sketches/')
        self.assertIsInstance(response, dict)

    def test_get_sketch(self):
        """Test to get a sketch."""
        sketch = self.api_client.get_sketch(1)
        self.assertIsInstance(sketch, sketch_lib.Sketch)
        self.assertEqual(sketch.id, 1)
        self.assertEqual(sketch.name, 'test')
        self.assertEqual(sketch.description, 'test')

    def test_get_sketches(self):
        """Test to get a list of sketches."""
        sketches = self.api_client.list_sketches()
        self.assertIsInstance(sketches, list)
        self.assertEqual(len(sketches), 1)
        self.assertIsInstance(sketches[0], sketch_lib.Sketch)