# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\tests\cv\test_frame.py
# Compiled at: 2020-04-10 08:59:09
# Size of source mod 2**32: 1361 bytes
"""
test module for reading in stream
"""
import unittest.mock as mock
import cv2
from sail_utils.cv.frame import ImageFileStreamer, LiveStreamer, VideoFileStreamer

@mock.patch('cv2.VideoCapture')
def test_live_streamer_init(mocked_video):
    """
    test live streamer construction
    :param mocked_video:
    :param mocked_time:
    :return:
    """
    streamer = LiveStreamer(source='test_stream', rate=15)
    assert mocked_video is cv2.VideoCapture
    assert streamer.rate == 15


@mock.patch('glob.glob', return_value=['file10', 'file1', 'file2'])
def test_image_files_streamer_init(mocked_files):
    """
    test image files streamer construction
    :param mocked_files:
    :return:
    """
    streamer = ImageFileStreamer('images_folder', suffix='.jpg', rate=2)
    assert streamer.stream == sorted((mocked_files()), key=(lambda x: (len(x), x)))
    assert streamer.rate == 2


@mock.patch('cv2.VideoCapture')
def test_video_file_streamer_init(mocked_video):
    """
    test video streamer construction
    :param mocked_video:
    :return:
    """
    streamer = VideoFileStreamer(source='test_video', rate=12)
    assert mocked_video is cv2.VideoCapture
    assert streamer.rate == 12