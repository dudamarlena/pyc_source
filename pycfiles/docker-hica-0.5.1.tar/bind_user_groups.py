# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/podvody/Repos/docker-hica/injectors/bind_user_groups.py
# Compiled at: 2015-09-24 04:54:10
from base.hica_base import *

class BindUsersGroupsInjector(HicaInjector):

    def get_description(self):
        return 'Bind mounts users and groups into the container'

    def get_config_key(self):
        return 'io.hica.bind_users_groups'

    def get_injected_args(self):
        return (
         (
          '--users-path', HicaValueType.PATH, '/etc/passwd'),
         (
          '--groups-path', HicaValueType.PATH, '/etc/group'))