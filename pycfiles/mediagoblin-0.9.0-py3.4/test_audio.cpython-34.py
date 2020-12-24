# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_audio.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3638 bytes
import tempfile, shutil, os, pytest
from contextlib import contextmanager
import logging, imghdr
pytest.importorskip('gi.repository.Gst')
pytest.importorskip('scikits.audiolab')
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
from mediagoblin.media_types.audio.transcoders import AudioTranscoder, AudioThumbnailer
from mediagoblin.media_types.tools import discover

@contextmanager
def create_audio():
    audio = tempfile.NamedTemporaryFile()
    src = Gst.ElementFactory.make('audiotestsrc', None)
    src.set_property('num-buffers', 50)
    enc = Gst.ElementFactory.make('flacenc', None)
    dst = Gst.ElementFactory.make('filesink', None)
    dst.set_property('location', audio.name)
    pipeline = Gst.Pipeline()
    pipeline.add(src)
    pipeline.add(enc)
    pipeline.add(dst)
    src.link(enc)
    enc.link(dst)
    pipeline.set_state(Gst.State.PLAYING)
    state = pipeline.get_state(3 * Gst.SECOND)
    assert state[0] == Gst.StateChangeReturn.SUCCESS
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(3 * Gst.SECOND, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)
    yield audio.name


@contextmanager
def create_data_for_test():
    with create_audio() as (audio_name):
        second_file = tempfile.NamedTemporaryFile()
        yield (audio_name, second_file.name)


def test_transcoder():
    """
    Tests AudioTransocder's transcode method
    """
    transcoder = AudioTranscoder()
    with create_data_for_test() as (audio_name, result_name):
        transcoder.transcode(audio_name, result_name, quality=0.3, progress_callback=None)
        info = discover(result_name)
        assert len(info.get_audio_streams()) == 1
        transcoder.transcode(audio_name, result_name, quality=0.3, mux_name='oggmux', progress_callback=None)
        info = discover(result_name)
        assert len(info.get_audio_streams()) == 1


def test_thumbnails():
    """Test thumbnails generation.

    The code below heavily repeats
    audio.processing.CommonAudioProcessor.create_spectrogram
    1. Create test audio
    2. Convert it to OGG source for spectogram using transcoder
    3. Create spectogram in jpg

    """
    thumbnailer = AudioThumbnailer()
    transcoder = AudioTranscoder()
    with create_data_for_test() as (audio_name, new_name):
        transcoder.transcode(audio_name, new_name, mux_name='oggmux')
        thumbnail = tempfile.NamedTemporaryFile(suffix='.jpg')
        thumbnailer.spectrogram(new_name, thumbnail.name, width=100, fft_size=4096)
        assert imghdr.what(thumbnail.name) == 'jpeg'