# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jorgeramos/Projects/uphold/aiopype/tests/sources/test_pusher.py
# Compiled at: 2016-07-05 12:54:49
# Size of source mod 2**32: 1007 bytes
__doc__ = '\nTest Pusher client source.\n'
import asyncio
from unittest import mock
from unittest import TestCase
from aiopype.sources import PusherClientSource

class TestPusherClientSource(TestCase):

    def test_start(self):
        mock_handler = mock.MagicMock()
        source = PusherClientSource('test', mock_handler)
        source.pusher = mock.MagicMock()
        type(source.pusher).exception = mock.PropertyMock(side_effect=[None, 'a', Exception('forcequit')])
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(source.start())
        except Exception as error:
            self.assertEqual(str(error), 'forcequit')

        self.assertTrue(source.done)
        type(source.pusher).exception = mock.PropertyMock(return_value=None)
        type(source.pusher.connection).state = mock.PropertyMock(return_value='failed')
        try:
            loop.run_until_complete(source.start())
        except Exception as error:
            self.assertEqual(str(error), 'Connection to pusherclient lost failed')