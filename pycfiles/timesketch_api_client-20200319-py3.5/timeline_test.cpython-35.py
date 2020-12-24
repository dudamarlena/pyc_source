# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/timeline_test.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 1442 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import unittest, mock
from . import client
from . import test_lib
from . import timeline as timeline_lib

class TimelineTest(unittest.TestCase):
    __doc__ = 'Test Timeline object.'

    @mock.patch('requests.Session', test_lib.mock_session)
    def setUp(self):
        """Setup test case."""
        self.api_client = client.TimesketchApi('http://127.0.0.1', 'test', 'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_timeline(self):
        """Test Timeline object."""
        timeline = self.sketch.list_timelines()[0]
        self.assertIsInstance(timeline, timeline_lib.Timeline)
        self.assertEqual(timeline.id, 1)
        self.assertEqual(timeline.name, 'test')
        self.assertEqual(timeline.index, 'test')