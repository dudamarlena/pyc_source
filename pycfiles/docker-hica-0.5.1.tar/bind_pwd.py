# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/bind_pwd.py
# Compiled at: 2015-10-26 10:04:39
import os
from base.hica_base import *

class BindPwdInjector(HicaInjector):

    def get_description(self):
        return ('Bind mounts current working directory ({0}) into the container').format(os.getenv('PWD'))

    def get_config_key(self):
        return 'io.hica.bind_pwd'

    def get_injected_args(self):
        return (
         (
          None, HicaValueType.PATH, os.getenv('PWD')),)

    def inject_config(self, config, args):
        super(BindPwdInjector, self).inject_config(config, args)
        config.append('-w')
        config.append(args[0][1])