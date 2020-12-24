# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/story_test.py
# Compiled at: 2020-03-13 10:57:40
# Size of source mod 2**32: 1995 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import unittest, mock
from . import client
from . import test_lib
from . import story as story_lib

class StoryTest(unittest.TestCase):
    __doc__ = 'Test Story object.'

    @mock.patch('requests.Session', test_lib.mock_session)
    def setUp(self):
        """Setup test case."""
        self.api_client = client.TimesketchApi('http://127.0.0.1', 'test', 'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_story(self):
        """Test story object."""
        story = self.sketch.list_stories()[0]
        self.assertIsInstance(story, story_lib.Story)
        self.assertEqual(story.id, 1)
        self.assertEqual(story.title, 'My First Story')
        self.assertEqual(len(story), 3)
        blocks = list(story.blocks)
        text_count = 0
        view_count = 0
        for block in blocks:
            if block.TYPE == 'text':
                text_count += 1
            elif block.TYPE == 'view':
                view_count += 1

        self.assertEqual(text_count, 2)
        self.assertEqual(view_count, 1)
        self.assertEqual(blocks[0].text, '# My Heading\nWith Some Text.')
        blocks[0].move_down()
        blocks = list(story.blocks)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[1].text, '# My Heading\nWith Some Text.')