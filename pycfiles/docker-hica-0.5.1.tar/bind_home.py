# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/bind_home.py
# Compiled at: 2015-09-24 04:53:47
import os
from base.hica_base import *

class BindHomeInjector(HicaInjector):

    def get_description(self):
        return ('Bind mounts home directory ({0}) into the container').format(os.getenv('HOME'))

    def get_config_key(self):
        return 'io.hica.bind_home'

    def get_injected_args(self):
        return (
         (
          '--home-path', HicaValueType.PATH, os.getenv('HOME')),)