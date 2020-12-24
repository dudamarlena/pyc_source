# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/sound_device.py
# Compiled at: 2015-09-24 04:55:12
from base.hica_base import *

class SoundDeviceInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts sound device into the container'

    def get_config_key(self):
        return 'io.hica.sound_device'

    def get_injected_args(self):
        return (
         (
          '--sound-device', HicaValueType.DEVICE | HicaValueType.GLOB, '/dev/snd*'),)