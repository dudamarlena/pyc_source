# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/dri_passthrough.py
# Compiled at: 2015-10-26 10:01:52
from base.hica_base import *

class DriPassthroughInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts direct rendering interface devices (DRI) into the container'

    def get_config_key(self):
        return 'io.hica.dri_passthrough'

    def get_injected_args(self):
        return (
         (
          '--dri-passthrough-path', HicaValueType.DEVICE | HicaValueType.GLOB, '/dev/dri/*'),
         (
          '--dri-passthrough-path-ati', HicaValueType.DEVICE | HicaValueType.GLOB, '/dev/ati/*'),
         (
          '--dri-passthrough-path-nvidia', HicaValueType.DEVICE | HicaValueType.GLOB, '/dev/nvidia/*'))