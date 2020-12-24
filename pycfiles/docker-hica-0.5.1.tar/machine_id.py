# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/machine_id.py
# Compiled at: 2015-09-24 04:55:03
from base.hica_base import *

class MachineIdInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts machine-id into the container'

    def get_config_key(self):
        return 'io.hica.machine_id'

    def get_injected_args(self):
        return (
         (
          '--machine-id-path', HicaValueType.PATH, '/etc/machine-id'),)