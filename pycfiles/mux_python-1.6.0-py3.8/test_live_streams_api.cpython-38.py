# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_live_streams_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 2536 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import unittest, mux_python
from mux_python.api.live_streams_api import LiveStreamsApi
from mux_python.rest import ApiException

class TestLiveStreamsApi(unittest.TestCase):
    __doc__ = 'LiveStreamsApi unit test stubs'

    def setUp(self):
        self.api = mux_python.api.live_streams_api.LiveStreamsApi()

    def tearDown(self):
        pass

    def test_create_live_stream(self):
        """Test case for create_live_stream

        Create a live stream  # noqa: E501
        """
        pass

    def test_create_live_stream_playback_id(self):
        """Test case for create_live_stream_playback_id

        Create a live stream playback ID  # noqa: E501
        """
        pass

    def test_create_live_stream_simulcast_target(self):
        """Test case for create_live_stream_simulcast_target

        Create a live stream simulcast target  # noqa: E501
        """
        pass

    def test_delete_live_stream(self):
        """Test case for delete_live_stream

        Delete a live stream  # noqa: E501
        """
        pass

    def test_delete_live_stream_playback_id(self):
        """Test case for delete_live_stream_playback_id

        Delete a live stream playback ID  # noqa: E501
        """
        pass

    def test_delete_live_stream_simulcast_target(self):
        """Test case for delete_live_stream_simulcast_target

        Delete a Live Stream Simulcast Target  # noqa: E501
        """
        pass

    def test_get_live_stream(self):
        """Test case for get_live_stream

        Retrieve a live stream  # noqa: E501
        """
        pass

    def test_get_live_stream_simulcast_target(self):
        """Test case for get_live_stream_simulcast_target

        Retrieve a Live Stream Simulcast Target  # noqa: E501
        """
        pass

    def test_list_live_streams(self):
        """Test case for list_live_streams

        List live streams  # noqa: E501
        """
        pass

    def test_reset_stream_key(self):
        """Test case for reset_stream_key

        Reset a live stream’s stream key  # noqa: E501
        """
        pass

    def test_signal_live_stream_complete(self):
        """Test case for signal_live_stream_complete

        Signal a live stream is finished  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()