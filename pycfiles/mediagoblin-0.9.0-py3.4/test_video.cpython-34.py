# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_video.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 5189 bytes
import tempfile, os
from contextlib import contextmanager
import imghdr, pytest
pytest.importorskip('gi.repository.Gst')
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
from mediagoblin.media_types.video.transcoders import capture_thumb, VideoTranscoder
from mediagoblin.media_types.tools import discover

@contextmanager
def create_data(suffix=None, make_audio=False):
    video = tempfile.NamedTemporaryFile()
    src = Gst.ElementFactory.make('videotestsrc', None)
    src.set_property('num-buffers', 10)
    videorate = Gst.ElementFactory.make('videorate', None)
    enc = Gst.ElementFactory.make('theoraenc', None)
    mux = Gst.ElementFactory.make('oggmux', None)
    dst = Gst.ElementFactory.make('filesink', None)
    dst.set_property('location', video.name)
    pipeline = Gst.Pipeline()
    pipeline.add(src)
    pipeline.add(videorate)
    pipeline.add(enc)
    pipeline.add(mux)
    pipeline.add(dst)
    src.link(videorate)
    videorate.link(enc)
    enc.link(mux)
    mux.link(dst)
    if make_audio:
        audio_src = Gst.ElementFactory.make('audiotestsrc', None)
        audio_src.set_property('num-buffers', 10)
        audiorate = Gst.ElementFactory.make('audiorate', None)
        audio_enc = Gst.ElementFactory.make('vorbisenc', None)
        pipeline.add(audio_src)
        pipeline.add(audio_enc)
        pipeline.add(audiorate)
        audio_src.link(audiorate)
        audiorate.link(audio_enc)
        audio_enc.link(mux)
    pipeline.set_state(Gst.State.PLAYING)
    state = pipeline.get_state(3 * Gst.SECOND)
    assert state[0] == Gst.StateChangeReturn.SUCCESS
    bus = pipeline.get_bus()
    message = bus.timed_pop_filtered(3 * Gst.SECOND, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)
    if suffix:
        result = tempfile.NamedTemporaryFile(suffix=suffix)
    else:
        result = tempfile.NamedTemporaryFile()
    yield (
     video.name, result.name)


def test_thumbnails():
    """
    Test thumbnails generation.
    1. Create a video (+audio) from gst's videotestsrc
    2. Capture thumbnail
    3. Everything should get removed because of temp files usage
    """
    test_formats = [
     ('.png', 'png'), ('.jpg', 'jpeg'), ('.gif', 'gif')]
    for suffix, format in test_formats:
        with create_data(suffix) as (video_name, thumbnail_name):
            capture_thumb(video_name, thumbnail_name, width=40)
            assert imghdr.what(thumbnail_name) == format

    suffix, format = test_formats[0]
    with create_data(suffix, True) as (video_name, thumbnail_name):
        capture_thumb(video_name, thumbnail_name, width=40)
        assert imghdr.what(thumbnail_name) == format
    with create_data(suffix, True) as (video_name, thumbnail_name):
        capture_thumb(video_name, thumbnail_name, width=10)
        assert imghdr.what(thumbnail_name) == format
    with create_data(suffix, True) as (video_name, thumbnail_name):
        capture_thumb(video_name, thumbnail_name, width=100)
        assert imghdr.what(thumbnail_name) == format


def test_transcoder():
    with create_data() as (video_name, result_name):
        transcoder = VideoTranscoder()
        transcoder.transcode(video_name, result_name, vp8_quality=8, vp8_threads=0, vorbis_quality=0.3, dimensions=(640,
                                                                                                                    640))
        assert len(discover(result_name).get_video_streams()) == 1
    with create_data(make_audio=True) as (video_name, result_name):
        transcoder = VideoTranscoder()
        transcoder.transcode(video_name, result_name, vp8_quality=8, vp8_threads=0, vorbis_quality=0.3, dimensions=(640,
                                                                                                                    640))
        assert len(discover(result_name).get_video_streams()) == 1
        assert len(discover(result_name).get_audio_streams()) == 1