# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/sketch_test.py
# Compiled at: 2020-01-28 06:06:27
# Size of source mod 2**32: 1745 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import unittest, mock
from . import client
from . import test_lib
from . import timeline as timeline_lib
from . import view as view_lib

class SketchTest(unittest.TestCase):
    __doc__ = 'Test Sketch object.'

    @mock.patch('requests.Session', test_lib.mock_session)
    def setUp(self):
        """Setup test case."""
        self.api_client = client.TimesketchApi('http://127.0.0.1', 'test', 'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_get_views(self):
        """Test to get a view."""
        views = self.sketch.list_views()
        self.assertIsInstance(views, list)
        self.assertEqual(len(views), 2)
        self.assertIsInstance(views[0], view_lib.View)

    def test_get_timelines(self):
        """Test to get a timeline."""
        timelines = self.sketch.list_timelines()
        self.assertIsInstance(timelines, list)
        self.assertEqual(len(timelines), 2)
        self.assertIsInstance(timelines[0], timeline_lib.Timeline)