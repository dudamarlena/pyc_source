# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ravijayanth/Desktop/project/library/Gender/mp3_to_wav.py
# Compiled at: 2019-11-06 02:22:35
import os
from subprocess import Popen

def convert_mp3_to_wav(filename):
    """
        Given an mp3 file, this function will create a corresponding .wav file in the same location where .mp3 file is there
        """
    if filename.endswith('.mp3'):
        a, b = filename.split('.')
        p = Popen(['ffmpeg -hide_banner -loglevel panic -i ' + filename + ' -acodec pcm_s16le -ac 1 -ar 16000 ' + a + ('.wav').format(filename)], shell=True)
        p.wait()