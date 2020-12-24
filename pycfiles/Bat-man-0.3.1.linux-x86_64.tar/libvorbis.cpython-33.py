# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/libvorbis.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 641 bytes
from batman.codec_interface import base_codec
from batman.codec_interface import ffmpeg_base_codec
import subprocess

class LibVorbis(ffmpeg_base_codec.FFMpegBaseAudioCodec):
    PRETTY_NAME = 'OGG(Vorbis)'
    TECHNICAL_NAME = 'libvorbis'
    SOLO_ENCODING = True

    def make_valid_file_name_from_caption(self, caption):
        return ffmpeg_base_codec.prepare_caption(caption) + '.ogg'

    def encode(self, out_path, avi_file):
        subprocess.call([self.ffmpeg_command, '-y', '-i', avi_file, '-vn', '-codec:a', 'libvorbis',
         '-qscale:a', '3', out_path])


base_codec.register_audio_codec(LibVorbis)