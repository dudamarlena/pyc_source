# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/xsocket.py
# Compiled at: 2015-10-13 06:07:12
import os
from base.hica_base import *

class XSocketInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts XSocket into the container'

    def get_config_key(self):
        return 'io.hica.xsocket_passthrough'

    def get_injected_args(self):
        return (
         (
          '--xsocket-path', HicaValueType.PATH, '/tmp/.X11-unix'),
         (
          '--x-display-num', HicaValueType.STRING, 'DISPLAY=' + os.getenv('DISPLAY')))