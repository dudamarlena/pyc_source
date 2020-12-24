# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/libx264_aac.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 999 bytes
from batman.codec_interface import base_codec, libx264, aac, ffmpeg_base_codec
import subprocess
from batman import definitions

class LibX264_AACInteractor(base_codec.Interactor):
    PRETTY_NAME = 'MP4(libx264/AAC)'

    def __init__(self):
        if definitions.WINDOWS:
            self.ffmpeg_command = definitions.path_with('bin', 'ffmpeg.exe')
        else:
            self.ffmpeg_command = 'ffmpeg'

    @staticmethod
    def can_be_used():
        return libx264.LibX264.can_be_used() and aac.AAC.can_be_used()

    def encode(self, out_path, avi_file):
        subprocess.call([self.ffmpeg_command, '-y', '-i', avi_file, '-codec:v', 'libx264',
         '-strict', '-2', '-codec:a', 'aac', out_path])

    def make_valid_file_name_from_caption(self, caption):
        return ffmpeg_base_codec.prepare_caption(caption) + '.mp4'


base_codec.register_interaction(libx264.LibX264, aac.AAC, LibX264_AACInteractor)