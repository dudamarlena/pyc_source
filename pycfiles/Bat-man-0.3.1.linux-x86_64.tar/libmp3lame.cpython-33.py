# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/libmp3lame.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 2196 bytes
from batman.codec_interface import base_codec
from batman import definitions
import os, re, subprocess, tempfile

class LibMP3Lame(base_codec.BaseAudioCodec):
    PRETTY_NAME = 'MP3(Lame)'
    TECHNICAL_NAME = 'libmp3lame'
    SOLO_ENCODING = True

    def __init__(self):
        if definitions.WINDOWS:
            self.lame_command = definitions.path_with('bin', 'lame.exe')
            self.ffmpeg_command = definitions.path_with('bin', 'ffmpeg.exe')
        else:
            self.lame_command = 'lame'
            self.ffmpeg_command = 'ffmpeg'

    @staticmethod
    def can_be_used():
        if not definitions.WINDOWS:
            return True
        else:
            lame_cmd = definitions.path_with('bin', 'lame.exe')
            ffmpeg_cmd = definitions.path_with('bin', 'ffmpeg.exe')
            if os.path.exists(lame_cmd) and os.path.exists(ffmpeg_cmd):
                return True
            return False

    def make_valid_file_name_from_caption(self, caption):
        caption = re.sub('\\/', '-', caption)
        caption = re.sub('"', '', caption)
        caption = re.sub("'", '', caption)
        caption = re.sub('[.]$', '', caption)
        caption = re.sub('[.]', '_', caption)
        treated_result = caption + '.mp3'
        return treated_result

    def encode(self, out_path, avi_file):
        if definitions.WINDOWS:
            wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            wav_file.close()
        else:
            wav_file = tempfile.NamedTemporaryFile(suffix='.wav')
        subprocess.call([self.ffmpeg_command, '-y', '-i', avi_file, '-vn',
         wav_file.name], stdout=subprocess.DEVNULL)
        subprocess.call([self.lame_command, '-V2', wav_file.name, out_path], stdout=subprocess.DEVNULL)
        if definitions.WINDOWS:
            os.unlink(wav_file.name)


base_codec.register_audio_codec(LibMP3Lame)