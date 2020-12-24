# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/media_tools.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2513 bytes
from contextlib import contextmanager
import tempfile, gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

@contextmanager
def create_av(make_video=False, make_audio=False):
    """creates audio/video in `path`, throws AssertionError on any error"""
    media = tempfile.NamedTemporaryFile(suffix='.ogg')
    pipeline = Gst.Pipeline()
    mux = Gst.ElementFactory.make('oggmux', 'mux')
    pipeline.add(mux)
    if make_video:
        video_src = Gst.ElementFactory.make('videotestsrc', 'video_src')
        video_src.set_property('num-buffers', 20)
        video_enc = Gst.ElementFactory.make('theoraenc', 'video_enc')
        pipeline.add(video_src)
        pipeline.add(video_enc)
        assert video_src.link(video_enc)
        assert video_enc.link(mux)
    if make_audio:
        audio_src = Gst.ElementFactory.make('audiotestsrc', 'audio_src')
        audio_src.set_property('num-buffers', 20)
        audio_enc = Gst.ElementFactory.make('vorbisenc', 'audio_enc')
        pipeline.add(audio_src)
        pipeline.add(audio_enc)
        assert audio_src.link(audio_enc)
        assert audio_enc.link(mux)
    sink = Gst.ElementFactory.make('filesink', 'sink')
    sink.set_property('location', media.name)
    pipeline.add(sink)
    mux.link(sink)
    pipeline.set_state(Gst.State.PLAYING)
    state = pipeline.get_state(Gst.SECOND)
    assert state[0] == Gst.StateChangeReturn.SUCCESS
    bus = pipeline.get_bus()
    message = bus.timed_pop_filtered(Gst.SECOND, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    assert message.type == Gst.MessageType.EOS
    pipeline.set_state(Gst.State.NULL)
    yield media.name