# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/theora_vorbis.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 1070 bytes
from batman.codec_interface import base_codec, libtheora, libvorbis, ffmpeg_base_codec
import subprocess
from batman import definitions

class TheoraVorbisInteractor(base_codec.Interactor):
    PRETTY_NAME = 'OGV(Theora/Vorbis)'

    def __init__(self):
        if definitions.WINDOWS:
            self.ffmpeg_command = definitions.path_with('bin', 'ffmpeg.exe')
        else:
            self.ffmpeg_command = 'ffmpeg'

    @staticmethod
    def can_be_used():
        return libtheora.LibTheora.can_be_used() and libvorbis.LibVorbis.can_be_used()

    def encode(self, out_path, avi_file):
        subprocess.call([self.ffmpeg_command, '-y', '-i', avi_file, '-codec:v', 'libtheora',
         '-qscale:v', '7', '-codec:a', 'libvorbis', '-qscale:a', '3', out_path])

    def make_valid_file_name_from_caption(self, caption):
        return ffmpeg_base_codec.prepare_caption(caption) + '.ogv'


base_codec.register_interaction(libtheora.LibTheora, libvorbis.LibVorbis, TheoraVorbisInteractor)