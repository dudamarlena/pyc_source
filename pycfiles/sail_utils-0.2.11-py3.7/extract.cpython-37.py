# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\audio\extract.py
# Compiled at: 2020-04-22 07:00:47
# Size of source mod 2**32: 525 bytes
"""
module for audio extraction
"""
from ffmpy import FFmpeg

def extract_audio(input_path: str, output_path: str, sample_rate: int=16000):
    """
    extract audio from the video
    :param input_path:
    :param output_path:
    :param sample_rate:
    :return:
    """
    ff_cmd = FFmpeg(global_options=['-y'], inputs={input_path: None},
      outputs={output_path: ['-f', 'wav', '-ar', (f"{sample_rate}"), '-ac', '1']})
    ff_cmd.run()