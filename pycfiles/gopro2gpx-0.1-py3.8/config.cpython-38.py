# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gopro2gpx/config.py
# Compiled at: 2020-04-24 06:28:49
# Size of source mod 2**32: 604 bytes
import os, platform, sys

class Config(object):

    def __init__(self, input_file, outputfile, format, verbose, skip):
        self.ffmpeg_cmd = os.getenv('FFMPEG_PATH', 'ffmpeg')
        self.ffprobe_cmd = os.getenv('FFPROBE_PATH', 'ffprobe')
        self.verbose = verbose
        self.format = format
        self.input_file = input_file
        self.output_file = outputfile
        self.skip = skip