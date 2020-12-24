# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/kvm_passthrough.py
# Compiled at: 2015-09-24 04:54:57
from base.hica_base import *

class KvmPassthroughInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts KVM device into the container'

    def get_config_key(self):
        return 'io.hica.kvm_passthrough'

    def get_injected_args(self):
        return (
         (
          '--kvm-device', HicaValueType.DEVICE, '/dev/kvm'),)