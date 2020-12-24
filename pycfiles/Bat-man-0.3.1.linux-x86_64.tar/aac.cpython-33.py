# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/aac.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 607 bytes
from batman.codec_interface import base_codec
from batman.codec_interface import ffmpeg_base_codec
import subprocess

class AAC(ffmpeg_base_codec.FFMpegBaseAudioCodec):
    PRETTY_NAME = 'AAC'
    TECHNICAL_NAME = 'aac'
    SOLO_ENCODING = True

    def make_valid_file_name_from_caption(self, caption):
        return ffmpeg_base_codec.prepare_caption(caption) + '.aac'

    def encode(self, out_path, avi_file):
        subprocess.call([self.ffmpeg_command, '-y', '-i', avi_file, '-vn',
         '-strict', '-2', '-codec:a', 'aac', out_path])


base_codec.register_audio_codec(AAC)