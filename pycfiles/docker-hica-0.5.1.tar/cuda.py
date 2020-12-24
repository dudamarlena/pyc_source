# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/cuda.py
# Compiled at: 2015-09-24 04:54:41
from base.hica_base import *

class CudaInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts CUDA devices into the container'

    def get_config_key(self):
        return 'io.hica.cuda'

    def get_injected_args(self):
        return (
         (
          '--cuda-device', HicaValueType.DEVICE, '/dev/nvidia0'),
         (
          '--cuda-device-ctl', HicaValueType.DEVICE, '/dev/nvidiactl'),
         (
          '--cuda-device-uvm', HicaValueType.DEVICE, '/dev/nvidia-uvm'))