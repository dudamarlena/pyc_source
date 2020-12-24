# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/util/__init__.py
# Compiled at: 2017-03-29 12:18:52
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import socket, subprocess, tempfile, os, os.path, psutil
from os.path import dirname
from onyx.util.log import getLogger
from onyx.config import get_config
LOGGER = getLogger(__name__)
config = get_config('onyx')

def play_wav(uri):
    play_cmd = config.get('Sound', 'wav')
    play_wav_cmd = str(play_cmd).split(' ')
    for index, cmd in enumerate(play_wav_cmd):
        if cmd == '#1':
            play_wav_cmd[index] = get_http(uri)

    return subprocess.Popen(play_wav_cmd)


def play_mp3(uri):
    play_cmd = config.get('Sound', 'mp3')
    play_mp3_cmd = str(play_cmd).split(' ')
    for index, cmd in enumerate(play_mp3_cmd):
        if cmd == '#1':
            play_mp3_cmd[index] = get_http(uri)

    return subprocess.Popen(play_mp3_cmd)


def get_http(uri):
    return uri.replace('https://', 'http://')