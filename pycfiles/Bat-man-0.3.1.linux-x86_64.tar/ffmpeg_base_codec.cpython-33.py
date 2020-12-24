# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/ffmpeg_base_codec.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 1653 bytes
from batman.codec_interface import base_codec
from batman import definitions
import re, os

def prepare_caption(caption):
    caption = re.sub('\\/', '-', caption)
    caption = re.sub('"', '', caption)
    caption = re.sub("'", '', caption)
    caption = re.sub('([?]|!)', '', caption)
    caption = re.sub('[.]$', '', caption)
    caption = re.sub('[.]', '_', caption)
    return caption


class FFMpegBaseAudioCodec(base_codec.BaseAudioCodec):

    def __init__(self):
        if definitions.WINDOWS:
            self.ffmpeg_command = definitions.path_with('bin', 'ffmpeg.exe')
        else:
            self.ffmpeg_command = 'ffmpeg'

    @staticmethod
    def can_be_used():
        if not definitions.WINDOWS:
            return True
        else:
            ffmpeg_cmd = definitions.path_with('bin', 'ffmpeg.exe')
            if os.path.exists(ffmpeg_cmd):
                return True
            return False


class FFMpegBaseVideoCodec(base_codec.BaseVideoCodec):

    def __init__(self):
        if definitions.WINDOWS:
            self.ffmpeg_command = definitions.path_with('bin', 'ffmpeg.exe')
        else:
            self.ffmpeg_command = 'ffmpeg'

    @staticmethod
    def can_be_used():
        if not definitions.WINDOWS:
            return True
        else:
            ffmpeg_cmd = definitions.path_with('bin', 'ffmpeg.exe')
            if os.path.exists(ffmpeg_cmd):
                return True
            return False