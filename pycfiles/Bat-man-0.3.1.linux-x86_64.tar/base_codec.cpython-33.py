# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/base_codec.py
# Compiled at: 2014-02-04 18:15:17
# Size of source mod 2**32: 4907 bytes
import glob, os, importlib, logging
CODEC_TYPE_VIDEO = 1
CODEC_TYPE_AUDIO = 2

class BaseAudioCodec(object):
    __doc__ = 'A Base for any implementation for a interface to a audio codec.\n    \n    Every audio interface should handle a ".wav" audio file and convert it\n    to the desired format.\n    \n    An audio codec can specify some settings, that will be shown at them\n    Preferences screen.(TODO.)\n    \n    '
    PRETTY_NAME = 'BaseAudioCodec'
    TECHNICAL_NAME = 'baseaudiocodec'
    SOLO_ENCODING = False

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def can_be_used():
        """Return True if this codec has everything it needs and can be used."""
        raise NotImplementedError()

    def make_valid_file_name_from_caption(self, caption):
        """Return a valid, usable, file name by the caption.
        
        Example: "Get Ready 2 Rokk" should return "Get Ready to Rokk.mp3"
        
        """
        raise NotImplementedError()

    def encode(self, out_path, wav_file):
        """Encode to out_path"""
        raise NotImplementedError()


class BaseVideoCodec(object):
    __doc__ = 'A Base for any implementation for a interface to a video codec.\n    \n    Every video codec should handle a ".avi" video file and convert it to the\n    desired format.\n    \n    A video codec can specify some settings.(TODO)\n    \n    '
    PRETTY_NAME = 'BaseVideoCodec'
    TECHNICAL_NAME = 'basevideocodec'
    SOLO_ENCODING = False

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def can_be_used():
        """Return True if this codec has everything it needs and can be used."""
        raise NotImplementedError()

    def make_valid_file_name_from_caption(self, caption):
        """Return a valid, usable, file name by the caption.
        
        Example: "Get Ready 2 Rokk" should return "Get Ready to Rokk.mp3"
        
        """
        raise NotImplementedError()

    def encode(self, out_path, avi_file):
        """Encode to out_path, using avi_file as source.
        
        This probably won't be called if SOLO_ENCODING is False.
                
        """
        raise NotImplementedError()


class Interactor(object):
    __doc__ = 'Interactor is a class that glues two codecs(video/audio).'
    PRETTY_NAME = ''

    @staticmethod
    def can_be_used():
        """Return True if this codec has everything it needs and can be used."""
        raise NotImplementedError()

    def encode(self, out_path, avi_file):
        raise NotImplementedError()

    def make_valid_file_name_from_caption(self, caption):
        raise NotImplementedError()


REGISTERED_AUDIO_CODECS = []
REGISTERED_VIDEO_CODECS = []
REGISTERED_INTERACTIONS = []

def register_audio_codec(audio_codec):
    if not audio_codec.can_be_used():
        logging.warning('Audio codec with technical name "{}" can\'t be used'.format(audio_codec.TECHNICAL_NAME))
        return
    REGISTERED_AUDIO_CODECS.append(audio_codec)


def register_video_codec(video_codec):
    if not video_codec.can_be_used():
        logging.warning('Video codec with technical name "{}" can\'t be used'.format(video_codec.TECHNICAL_NAME))
        return
    REGISTERED_VIDEO_CODECS.append(video_codec)


def register_interaction(video_codec, audio_codec, interactor):
    if not interactor.can_be_used():
        logging.warning('Interactor with name "{}" can\'t be used'.format(interactor))
    REGISTERED_INTERACTIONS.append([(video_codec, audio_codec), interactor])


def find_audio_codec_by_technical_name(technical_name):
    for codec in REGISTERED_AUDIO_CODECS:
        if codec.TECHNICAL_NAME == technical_name:
            return codec

    return


def find_video_codec_by_technical_name(technical_name):
    for codec in REGISTERED_VIDEO_CODECS:
        if codec.TECHNICAL_NAME == technical_name:
            return codec

    return


def find_interactor(video_codec, audio_codec):
    for interactor in REGISTERED_INTERACTIONS:
        if interactor[0][0] == audio_codec and interactor[0][1] == video_codec:
            return interactor[1]

    return


def is_codec_an_audio_codec(codec):
    if codec in REGISTERED_AUDIO_CODECS:
        return True
    for c in REGISTERED_AUDIO_CODECS:
        if isinstance(codec, c):
            return True

    return False


def is_codec_a_video_codec(codec):
    if codec in REGISTERED_VIDEO_CODECS:
        return True
    for c in REGISTERED_VIDEO_CODECS:
        if isinstance(codec, c):
            return True

    return False